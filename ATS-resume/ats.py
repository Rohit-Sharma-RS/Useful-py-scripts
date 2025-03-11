import os
import re
import PyPDF2
import pandas as pd
import requests
from io import BytesIO
from collections import defaultdict
import nltk
import docx
import tempfile
from urllib.parse import urlparse, parse_qs
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class ResumeATS:
    def __init__(self):
        # Define skill categories and keywords
        self.skill_categories = {
            'scraping': ['web scraping', 'scraping', 'beautifulsoup', 'selenium', 'scrapy', 'parsing'],
            'data_insights': ['data analysis', 'data visualization', 'dashboard', 'insights', 'analytics', 'tableau', 'power bi', 'looker'],
            'machine_learning': ['machine learning', 'ml', 'ai', 'artificial intelligence', 'model', 'algorithm', 'tensorflow', 'pytorch', 'scikit-learn'],
            'python': ['python', 'pandas', 'numpy', 'scipy', 'jupyter', 'pyspark'],
            'backend': ['backend', 'api', 'rest', 'flask', 'django', 'fastapi', 'sql', 'database', 'nosql'],
            'frontend': ['react', 'javascript', 'html', 'css', 'frontend', 'ui', 'ux'],
        }
        
        self.education_keywords = ['bachelor', 'master', 'phd', 'degree', 'b.tech', 'm.tech', 'b.e', 'm.e', 'bsc', 'msc']
        
        self.experience_keywords = ['experience', 'work', 'internship', 'data engineer', 'data analyst', 'project']
        
        self.weights = {
            'scraping': 0.15,
            'data_insights': 0.15,
            'machine_learning': 0.20,
            'python': 0.20,
            'backend': 0.15,
            'frontend': 0.05,
            'education': 0.05,
            'experience': 0.05
        }

    def extract_google_drive_id(self, url):
        """Extract file ID from Google Drive link"""
        parsed_url = urlparse(url)
        if 'drive.google.com' in parsed_url.netloc:
            if '/file/d/' in url:
                # Handle /file/d/ format
                file_id = url.split('/file/d/')[1].split('/')[0]
            elif 'id=' in url:
                # Handle id= format
                file_id = parse_qs(parsed_url.query).get('id', [None])[0]
            else:
                return None
            return file_id
        return None

    def download_google_drive_file(self, url):
        """Download file from Google Drive and return content"""
        file_id = self.extract_google_drive_id(url)
        if not file_id:
            raise ValueError(f"Could not extract Google Drive ID from {url}")
        
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(download_url, stream=True)
        
        # Check if the file is too large and requires confirmation
        if "confirm=" in response.url:
            confirm_token = response.url.split("confirm=")[1].split("&")[0]
            download_url = f"{download_url}&confirm={confirm_token}"
            response = requests.get(download_url, stream=True)
        
        return BytesIO(response.content)

    def extract_text_from_pdf(self, pdf_content):
        """Extract text from PDF content"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_content)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.lower()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self, docx_content):
        """Extract text from DOCX content"""
        try:
            # Save the content to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(docx_content.getvalue())
                temp_path = temp_file.name
            
            doc = docx.Document(temp_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            # Clean up
            os.unlink(temp_path)
            
            return text.lower()
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""

    def extract_text_from_document(self, doc_path_or_url):
        """Extract text from document (PDF or DOCX, local or URL)"""
        try:
            # Handle Google Drive links
            if 'drive.google.com' in doc_path_or_url:
                file_content = self.download_google_drive_file(doc_path_or_url)
                filename = doc_path_or_url
            # Handle direct URLs
            elif doc_path_or_url.startswith('http'):
                response = requests.get(doc_path_or_url)
                file_content = BytesIO(response.content)
                filename = doc_path_or_url
            # Handle local files
            else:
                with open(doc_path_or_url, 'rb') as f:
                    file_content = BytesIO(f.read())
                filename = doc_path_or_url
            
            # Determine file type and extract text
            if filename.lower().endswith('.pdf') or doc_path_or_url.lower().endswith('.pdf'):
                return self.extract_text_from_pdf(file_content)
            elif filename.lower().endswith('.docx') or doc_path_or_url.lower().endswith('.docx'):
                return self.extract_text_from_docx(file_content)
            else:
                # Try PDF first, then DOCX if that fails
                try:
                    return self.extract_text_from_pdf(file_content)
                except:
                    try:
                        file_content.seek(0)  # Reset file pointer
                        return self.extract_text_from_docx(file_content)
                    except:
                        raise ValueError("Unsupported file format")
                        
        except Exception as e:
            print(f"Error processing {doc_path_or_url}: {e}")
            return ""

    def analyze_resume(self, text):
        scores = {}
        
        # Score each skill category
        for category, keywords in self.skill_categories.items():
            category_score = 0
            for keyword in keywords:
                matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
                if matches > 0:
                    category_score += min(matches, 3)
            
            scores[category] = min(10, category_score * 3.33)
        
        # Score education
        education_score = 0
        for keyword in self.education_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                education_score += 2
        scores['education'] = min(10, education_score)
        
        # Score experience (with emphasis on data roles)
        experience_score = 0
        for keyword in self.experience_keywords:
            matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
            if matches > 0:
                # Give more weight to data-specific experience
                if 'data' in keyword:
                    experience_score += matches * 3
                else:
                    experience_score += matches
        scores['experience'] = min(10, experience_score)
        
        return scores

    def calculate_total_score(self, scores):
        """Calculate weighted total score"""
        total_score = 0
        for category, score in scores.items():
            total_score += score * self.weights.get(category, 0)
        
        # Scale to 0-100
        return round(total_score * 10, 1)

    def extract_contact_info(self, text):
        """Extract basic contact info from resume"""
        info = {}
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            info['email'] = email_match.group(0)
        
        # Extract phone number
        phone_match = re.search(r'\b(?:\+\d{1,3}[-\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
        if phone_match:
            info['phone'] = phone_match.group(0)
            
        # Try to extract name (simple heuristic - typically at the beginning)
        lines = text.split('\n')
        for line in lines[:5]:  # Check first few lines
            line = line.strip()
            if 2 <= len(line.split()) <= 5 and not re.search(r'@|\d', line):
                info['name'] = line.title()
                break
                
        return info

    def get_keywords_found(self, text):
        """Get all matching keywords from the resume"""
        all_keywords = {}
        for category, keywords in self.skill_categories.items():
            found = []
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                    found.append(keyword)
            if found:
                all_keywords[category] = found
        return all_keywords

    def evaluate_resume(self, doc_path_or_url):
        """Evaluate a single resume from document path or URL"""
        try:
            text = self.extract_text_from_document(doc_path_or_url)
            if not text:
                return {
                    'file': os.path.basename(doc_path_or_url) if not doc_path_or_url.startswith('http') else doc_path_or_url,
                    'error': 'Could not extract text from document',
                    'ats_score': 0
                }
                
            scores = self.analyze_resume(text)
            total_score = self.calculate_total_score(scores)
            contact_info = self.extract_contact_info(text)
            keywords_found = self.get_keywords_found(text)
            
            # Generate strengths and weaknesses
            strengths = [cat for cat, score in scores.items() if score >= 7]
            weaknesses = [cat for cat, score in scores.items() if score <= 3]
            
            # ATS recommendations
            recommendations = []
            if total_score < 70:
                if len(weaknesses) > 0:
                    recommendations.append(f"Add more keywords related to: {', '.join(weaknesses)}")
                recommendations.append("Include more specific technical skills and tools")
            if 'education' in weaknesses:
                recommendations.append("Add more details about your education")
            if 'experience' in weaknesses:
                recommendations.append("Expand on your work experience with concrete achievements")
            
            return {
                'file': os.path.basename(doc_path_or_url) if not doc_path_or_url.startswith('http') else doc_path_or_url,
                'contact_info': contact_info,
                'category_scores': scores,
                'ats_score': total_score,
                'keywords_found': keywords_found,
                'strengths': strengths,
                'weaknesses': weaknesses,
                'recommendations': recommendations
            }
        except Exception as e:
            return {
                'file': os.path.basename(doc_path_or_url) if not doc_path_or_url.startswith('http') else doc_path_or_url,
                'error': f"Failed to process document: {str(e)}",
                'ats_score': 0
            }

    def batch_evaluate(self, doc_paths_or_urls):
        """Evaluate multiple resumes and return results as a DataFrame"""
        results = []
        
        for doc in doc_paths_or_urls:
            result = self.evaluate_resume(doc)
            results.append(result)
            
        # Sort results by ATS score in descending order
        results.sort(key=lambda x: x['ats_score'], reverse=True)
        
        return results

# Example usage
if __name__ == "__main__":
    # Example list of resume docs
    resumes = ['https://drive.google.com/open?id=1rQREIWGXY0_R4_UpNS-OQuNv028ufAI4', 'https://drive.google.com/open?id=1_UE6Xn9ZQrZoyvpeZwuwxSma8kkldGMO', 'https://drive.google.com/open?id=1EuV5UBL1T5k_4GWyDwvxhlcXFe9aRUsV', 'https://drive.google.com/open?id=1bOwfKd5z7RnUsQo94VYVViIqjQ0tnGxV', 'https://drive.google.com/open?id=1YXHN62GwwRxilMyjlmyXdh8WIDTLqKUc', 'https://drive.google.com/open?id=1ogERna8_c9jtTPVQ1RJUP9qKiN2T1CCP', 'https://drive.google.com/open?id=1bfxy_87aF8Gms4CfyybBdQykOTDbWsMm', 'https://drive.google.com/open?id=1RmYqwRT3dAI6NOe2NikKOFXU93zAsyyf', 'https://drive.google.com/open?id=1SixlAMEn4RzcDKUYm6--6AhPBPkfIp25', 'https://drive.google.com/open?id=1rkIwL8ZKtuTZbCpfinXOQi7bBu1gLdJu', 'https://drive.google.com/open?id=1LOyBidLoHbuyjb42ENi1k_A3kxgiePtE', 'https://drive.google.com/open?id=1Y5TCoyNLXPp06v0a2NjNMxPcYhaccPKb', 'https://drive.google.com/open?id=1DYwzw1ROvBJjqq5HlWabC2kC_9h18OUF', 'https://drive.google.com/open?id=14v6FQyuQDE5HzYRHQpa5JRiLezUUrQkI', 'https://drive.google.com/open?id=1HitMrEh-609-T9TQbGda04lL_P9sSMBJ']
    
    ats = ResumeATS()
    results = ats.batch_evaluate(resumes)
    
    # Print results
    print(f"Evaluated {len(results)} resumes.")
    print("\nTop candidates:")
    for i, result in enumerate(results[:15]):  # Show top 15
        if 'error' in result:
            print(f"{i+1}. {result['file']} - Error: {result['error']}")
        else:
            print(f"{i+1}. {result.get('contact_info', {}).get('name', 'Unknown')} - Score: {result['ats_score']}/100")
    
    # Save detailed results to CSV
    df = pd.DataFrame(results)
    df.to_csv("ats_results.csv", index=False)
    print("\nDetailed results saved to ats_results.csv")