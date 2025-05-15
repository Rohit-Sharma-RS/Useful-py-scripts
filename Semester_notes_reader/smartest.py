import re
import time
import os
import nltk
from nltk.tokenize import sent_tokenize
import logging
import threading
import pyttsx3
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, font
from tkinter.messagebox import showinfo, showerror, askyesno
import PyPDF2
from pydub import AudioSegment

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmartReader:
    def __init__(self, root=None):
        # Initialize GUI if root is provided
        self.root = root
        self.text_widget = None
        self.control_frame = None
        self.status_var = None
        self.is_reading = False
        self.reading_thread = None
        self.stop_requested = False
        self.audio_save_path = None
        
        # Initialize pyttsx3
        self.engine = pyttsx3.init()
        
        # Set up event handlers for the speech engine
        self.engine.connect('started-utterance', self.on_started_utterance)
        self.engine.connect('finished-utterance', self.on_finished_utterance)
        
        # Ensure required NLTK data is available
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logging.info("Downloading required NLTK data...")
            nltk.download('punkt', quiet=True)
        
        # Define patterns for emphasis and pausing
        self.emphasis_patterns = [
            r'\*\*(.*?)\*\*',                 # Bold text: **important text**
            r'_([^_]+)_',                     # Italics: _emphasized text_
            r'#+ (.*?)(?:\n|$)',              # Headings: # Heading
            r'[A-Z][A-Z\s]+[A-Z]',            # All caps words: IMPORTANT
            r'\d+\.\d+(?:\.\d+)*',            # Section numbers: 2.1, 3.2.1
            r'[\w-]+\([\w, ]+\)',             # Functions: function(args)
            r'[\w-]+\[[\w, ]+\]',             # Array notations: array[index]
            r'[\w-]+:',                       # Definitions: Term:
        ]
        
        self.pause_patterns = [
            r'\.\s+',                         # End of sentence
            r'\n\n+',                         # Paragraph breaks
            r':\s+',                          # Before lists or explanations
            r',\s+',                          # Commas
            r';\s+',                          # Semicolons
            r'\*\*.*?\*\*\s+',                # After bold text
            r'#+ .*?(?:\n|$)',                # After headings
        ]
        
        # Define pause durations (in seconds)
        self.pause_durations = {
            'short': 0.2,   # Comma, semicolon
            'medium': 0.5,  # End of sentence, colon
            'long': 1.0,    # Paragraph break, after headings
        }
        
        # Reading speeds
        self.reading_speeds = {
            'slow': 150,     # Words per minute
            'normal': 200,
            'fast': 250
        }
        
        # Set default properties
        self.engine.setProperty('rate', self.reading_speeds['normal'])
        self.current_speed = 'normal'
        
        # Get available voices
        self.voices = self.engine.getProperty('voices')
        self.voice_index = 0  # Default to first voice
        if self.voices:
            self.engine.setProperty('voice', self.voices[self.voice_index].id)
            
        # Initialize current reading position trackers
        self.current_chunk_index = 0
        self.current_sentence_index = 0
        self.sentences = []
        self.chunks = []
        
    def on_started_utterance(self, name):
        """Callback when speech engine starts speaking"""
        if self.status_var:
            self.status_var.set("Speaking...")
    
    def on_finished_utterance(self, name, completed):
        """Callback when speech engine finishes speaking"""
        if self.status_var:
            self.status_var.set("Ready")

    def setup_gui(self):
        """Set up the GUI components"""
        if not self.root:
            return
            
        # Configure root window
        self.root.title("Smart Educational Text Reader")
        self.root.geometry("900x700")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # Create file menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PDF/Text", command=self.open_file)
        file_menu.add_command(label="Save Audio As...", command=self.save_audio_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Create voice settings menu
        voice_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Voice", menu=voice_menu)
        
        # Add voice options
        for i, voice in enumerate(self.voices):
            voice_menu.add_command(
                label=f"{voice.name}",
                command=lambda idx=i: self.change_voice(idx)
            )
        
        # Create speed menu
        speed_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Speed", menu=speed_menu)
        for speed in self.reading_speeds.keys():
            speed_menu.add_command(
                label=speed.capitalize(),
                command=lambda s=speed: self.change_speed(s)
            )
        
        # Create status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create text display area with syntax highlighting capability
        text_frame = ttk.LabelFrame(main_frame, text="Text Display", padding="5")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create text widget with scrollbar
        self.text_widget = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 12),
            background="#F5F5F5",
            foreground="#333333",
            insertbackground="#333333",
            selectbackground="#4A6984",
            selectforeground="#FFFFFF",
            padx=10,
            pady=10
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for text highlighting
        self.text_widget.tag_configure("highlight", background="#FFFF99")
        self.text_widget.tag_configure("emphasis", font=("Segoe UI", 12, "bold"), foreground="#0066CC")
        self.text_widget.tag_configure("normal", font=("Segoe UI", 12))
        self.text_widget.tag_configure("header", font=("Segoe UI", 14, "bold"), foreground="#003366")
        
        # Create control frame
        self.control_frame = ttk.Frame(main_frame)
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # Create control buttons
        btn_style = ttk.Style()
        btn_style.configure("Control.TButton", font=("Segoe UI", 10))
        
        btn_prev = ttk.Button(
            self.control_frame, 
            text="Previous", 
            command=self.previous_segment,
            style="Control.TButton"
        )
        btn_prev.pack(side=tk.LEFT, padx=5)
        
        btn_play_pause = ttk.Button(
            self.control_frame, 
            text="Play/Pause", 
            command=self.toggle_playback,
            style="Control.TButton"
        )
        btn_play_pause.pack(side=tk.LEFT, padx=5)
        
        btn_next = ttk.Button(
            self.control_frame, 
            text="Next", 
            command=self.next_segment,
            style="Control.TButton"
        )
        btn_next.pack(side=tk.LEFT, padx=5)
        
        btn_stop = ttk.Button(
            self.control_frame, 
            text="Stop", 
            command=self.stop_reading,
            style="Control.TButton"
        )
        btn_stop.pack(side=tk.LEFT, padx=5)
        
        # Save Audio button
        btn_save_audio = ttk.Button(
            self.control_frame,
            text="Save Audio",
            command=self.save_audio_dialog,
            style="Control.TButton"
        )
        btn_save_audio.pack(side=tk.LEFT, padx=(20, 5))
        
        # Voice selection combobox
        voice_label = ttk.Label(self.control_frame, text="Voice:")
        voice_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.voice_var = tk.StringVar()
        voice_combobox = ttk.Combobox(
            self.control_frame, 
            textvariable=self.voice_var,
            state="readonly",
            width=20
        )
        voice_options = [voice.name for voice in self.voices]
        voice_combobox['values'] = voice_options
        if voice_options:
            voice_combobox.current(self.voice_index)
        voice_combobox.pack(side=tk.LEFT, padx=5)
        voice_combobox.bind('<<ComboboxSelected>>', self.on_voice_selected)
        
        # Speed selection combobox
        speed_label = ttk.Label(self.control_frame, text="Speed:")
        speed_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.speed_var = tk.StringVar(value=self.current_speed.capitalize())
        speed_combobox = ttk.Combobox(
            self.control_frame, 
            textvariable=self.speed_var,
            state="readonly",
            width=10
        )
        speed_combobox['values'] = [s.capitalize() for s in self.reading_speeds.keys()]
        speed_combobox.pack(side=tk.LEFT, padx=5)
        speed_combobox.bind('<<ComboboxSelected>>', self.on_speed_selected)
        
    def wav_to_mp3(self, wav_path, mp3_path):
        """Convert WAV file to MP3 format using pydub"""
        try:
            audio = AudioSegment.from_wav(wav_path)
            audio.export(mp3_path, format="mp3")
            logging.info(f"Successfully converted {wav_path} to {mp3_path}")
            return True
        except Exception as e:
            logging.error(f"Error in wav_to_mp3 conversion: {e}")
            raise


    def save_audio_dialog(self):
        """Show dialog to save audio to file"""
        if not self.text_widget or not self.text_widget.get("1.0", tk.END).strip():
            if self.root:
                showerror("Error", "No text loaded to save as audio.")
            else:
                print("Error: No text loaded to save as audio.")
            return
        
        file_path = None
        if self.root:
            file_path = filedialog.asksaveasfilename(
                title="Save Audio As",
                defaultextension=".wav",
                filetypes=[("WAV Files", "*.wav"), ("MP3 Files", "*.mp3"), ("All Files", "*.*")]
            )
        else:
            file_path = input("Enter the path to save audio file (e.g., output.wav or output.mp3): ")
        
        if file_path:
            self.audio_save_path = file_path
            if self.root:
                self.status_var.set(f"Audio will be saved to: {file_path}")
            else:
                print(f"Audio will be saved to: {file_path}")
            return True
        return False
        
    def save_audio_to_file(self, text, file_path):
        """Save text as audio to a file, converting to MP3 if needed"""
        try:
            # Preprocess text
            text = self.preprocess_text(text)
            # Split into chunks for better memory management
            chunks = self.split_into_chunks(text)
            logging.info(f"Saving audio to: {file_path}")

            # Check if MP3 format is requested
            is_mp3 = file_path.lower().endswith('.mp3')
            temp_wav_path = None
            
            if is_mp3:
                temp_wav_path = file_path[:-4] + "_temp.wav"
                output_path = temp_wav_path
            else:
                output_path = file_path
            
            # Save as WAV (either final format or temporary)
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            # Convert to MP3 if needed
            if is_mp3:
                try:
                    logging.info(f"Converting WAV to MP3: {temp_wav_path} -> {file_path}")
                    self.wav_to_mp3(temp_wav_path, file_path)
                    
                    # Remove temporary WAV file
                    os.remove(temp_wav_path)
                    logging.info("Temporary WAV file removed")
                    
                except Exception as e:
                    logging.error(f"Error converting WAV to MP3: {e}")
                    if self.root:
                        showerror("Error", f"Failed to convert to MP3: {e}\nSaving as WAV instead.")
                        # If MP3 conversion fails, keep the WAV file
                        os.rename(temp_wav_path, file_path[:-4] + ".wav")
                    else:
                        print(f"Error: Failed to convert to MP3: {e}")
                        print(f"Saving as WAV instead: {file_path[:-4]}.wav")
                        os.rename(temp_wav_path, file_path[:-4] + ".wav")
                    return False
            
            logging.info("Audio saved successfully")
            if self.root:
                showinfo("Success", f"Audio saved successfully to {file_path}")
            else:
                print(f"Audio saved successfully to {file_path}")
            return True

        except Exception as e:
            logging.error(f"Error saving audio to file: {e}")
            if self.root:
                showerror("Error", f"Failed to save audio: {e}")
            else:
                print(f"Error: Failed to save audio: {e}")
            return False
    def open_file(self):
        """Open a file dialog to select a PDF or text file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF or Text File",
            filetypes=[
                ("PDF Files", "*.pdf"), 
                ("Text Files", "*.txt"), 
                ("Markdown Files", "*.md"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.process_file_gui(file_path)
    
    def process_file_gui(self, file_path):
        """Process a file and display it in the GUI"""
        try:
            # Extract text
            if file_path.lower().endswith('.pdf'):
                text = self.extract_text_from_pdf(file_path)
            elif file_path.lower().endswith(('.txt', '.md')):
                text = self.read_text_file(file_path)
            else:
                showerror("Error", "Unsupported file format. Please use PDF or TXT files.")
                return
                
            if not text:
                showerror("Error", "Failed to extract text from the file.")
                return
                
            # Clear existing text
            if self.text_widget:
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", text)
                
            # Store text for processing
            self.preprocess_and_split_text(text)
            
            # Update status
            if self.status_var:
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
                
            # Ask if the user wants to save as audio or read now
            user_choice = askyesno(
                "Audio Options",
                "Do you want to save this text as an audio file?\n\nChoose 'Yes' to save as audio, or 'No' to read it now."
            )
            
            if user_choice:
                # Save as audio
                if self.save_audio_dialog():
                    self.save_audio_to_file(text, self.audio_save_path)
            else:
                # Start reading
                self.is_reading = True
                self.current_sentence_index = 0
                self.highlight_current_sentence()
                self.read_current_sentence()
            
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            showerror("Error", f"An error occurred: {e}")
    
    def preprocess_and_split_text(self, text):
        """Preprocess the text and split into sentences for reading"""
        processed = self.preprocess_text(text)
        self.sentences = sent_tokenize(processed)
        self.current_sentence_index = 0
        logging.info(f"Text split into {len(self.sentences)} sentences")
    
    def highlight_current_sentence(self):
        """Highlight the current sentence in the text widget"""
        if not self.text_widget or not self.sentences or self.current_sentence_index >= len(self.sentences):
            return
            
        # Remove previous highlight
        self.text_widget.tag_remove("highlight", "1.0", tk.END)
        
        # Get current sentence
        current = self.sentences[self.current_sentence_index]
        
        # Find and highlight
        start_pos = "1.0"
        while True:
            pos = self.text_widget.search(current, start_pos, tk.END, nocase=True)
            if not pos:
                break
                
            end_pos = f"{pos}+{len(current)}c"
            self.text_widget.tag_add("highlight", pos, end_pos)
            self.text_widget.see(pos)  # Scroll to the highlighted text
            
            # Only highlight the first occurrence
            break
    
    def read_current_sentence(self):
        """Read the current sentence aloud"""
        if not self.sentences or self.current_sentence_index >= len(self.sentences):
            self.is_reading = False
            return
            
        # Get current sentence
        current = self.sentences[self.current_sentence_index]
        
        # Add markup for emphasis and pauses
        marked_text = self.add_markup(current)
        
        # Start reading in a separate thread
        self.reading_thread = threading.Thread(
            target=self.speak_with_effects,
            args=(marked_text, self.current_speed)
        )
        self.reading_thread.daemon = True
        self.reading_thread.start()
        
        # Wait for speech to finish then move to next sentence
        def check_speech_done():
            if not self.reading_thread.is_alive() and self.is_reading and not self.stop_requested:
                self.current_sentence_index += 1
                if self.current_sentence_index < len(self.sentences):
                    self.highlight_current_sentence()
                    self.read_current_sentence()
                else:
                    if self.status_var:
                        self.status_var.set("Reading completed")
                    self.is_reading = False
            
            # Continue checking if still reading
            if self.is_reading and not self.stop_requested:
                if self.root:
                    self.root.after(100, check_speech_done)
        
        # Start checking if speech is done
        if self.root:
            self.root.after(100, check_speech_done)
    
    def on_voice_selected(self, event):
        """Handle voice selection from combobox"""
        selected_voice = self.voice_var.get()
        for i, voice in enumerate(self.voices):
            if voice.name == selected_voice:
                self.change_voice(i)
                break
    
    def on_speed_selected(self, event):
        """Handle speed selection from combobox"""
        selected_speed = self.speed_var.get().lower()
        self.change_speed(selected_speed)
    
    def change_voice(self, voice_index):
        """Change the TTS voice"""
        if 0 <= voice_index < len(self.voices):
            self.voice_index = voice_index
            self.engine.setProperty('voice', self.voices[voice_index].id)
            if self.status_var:
                self.status_var.set(f"Voice changed to: {self.voices[voice_index].name}")
    
    def change_speed(self, speed):
        """Change the reading speed"""
        if speed in self.reading_speeds:
            self.current_speed = speed
            self.engine.setProperty('rate', self.reading_speeds[speed])
            if self.status_var:
                self.status_var.set(f"Speed changed to: {speed}")
    
    def toggle_playback(self):
        """Toggle between play and pause"""
        if self.is_reading:
            self.pause_reading()
        else:
            self.resume_reading()
    
    def pause_reading(self):
        """Pause the reading"""
        if self.is_reading:
            self.engine.stop()
            self.is_reading = False
            if self.status_var:
                self.status_var.set("Paused")
    
    def resume_reading(self):
        """Resume the reading"""
        if not self.is_reading and self.sentences:
            self.is_reading = True
            self.read_current_sentence()
    
    def stop_reading(self):
        """Stop the reading completely"""
        self.stop_requested = True
        self.engine.stop()
        self.is_reading = False
        if self.status_var:
            self.status_var.set("Stopped")
    
    def previous_segment(self):
        """Go to the previous sentence or chunk"""
        self.engine.stop()
        if self.current_sentence_index > 0:
            self.current_sentence_index -= 1
            self.highlight_current_sentence()
            if self.is_reading:
                self.read_current_sentence()
    
    def next_segment(self):
        """Go to the next sentence or chunk"""
        self.engine.stop()
        if self.current_sentence_index < len(self.sentences) - 1:
            self.current_sentence_index += 1
            self.highlight_current_sentence()
            if self.is_reading:
                self.read_current_sentence()

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file"""
        try:
            # Normalize path (handle Windows backslashes)
            pdf_path = os.path.normpath(pdf_path)
            
            logging.info(f"Opening PDF: {pdf_path}")
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text()
                logging.info(f"Successfully extracted text from {len(reader.pages)} pages")
                return text
        except FileNotFoundError:
            logging.error(f"File not found: {pdf_path}")
            if self.root:
                showerror("Error", f"Could not find the file at '{pdf_path}'")
            else:
                print(f"Error: Could not find the file at '{pdf_path}'")
            return None
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {e}")
            if self.root:
                showerror("Error", f"Error processing PDF: {e}")
            else:
                print(f"Error processing PDF: {e}")
            return None

    def read_text_file(self, txt_path):
        """Read text from a plain text file"""
        try:
            logging.info(f"Opening text file: {txt_path}")
            # Use raw string to handle Windows backslashes properly
            with open(txt_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except UnicodeDecodeError:
            # Try another common encoding if UTF-8 fails
            try:
                with open(txt_path, 'r', encoding='latin-1') as file:
                    text = file.read()
                logging.info("Successfully read file using latin-1 encoding")
                return text
            except Exception as e:
                logging.error(f"Error reading text file with alternate encoding: {e}")
                return None
        except Exception as e:
            logging.error(f"Error reading text file: {e}")
            return None
    
    def preprocess_text(self, text):
        """Clean and preprocess the text"""
        logging.info("Starting preprocessing...")

        # 1. Remove code blocks (```...``` and `...`)
        # Multi-line code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Inline code
        text = re.sub(r'`[^`]*`', '', text)

        # 2. Remove HTML tags (as Markdown can contain HTML)
        text = re.sub(r'<[^>]+>', '', text)

        # 3. Handle headings (remove #, but keep text)
        text = re.sub(r'^\s*#+\s+', '', text, flags=re.MULTILINE) # Remove leading #s

        # 4. Handle bold and italics
        # **bold** or __bold__
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'__(.*?)__', r'\1', text)
        # *italic* or _italic_
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'_(.*?)_', r'\1', text) # Be careful if underscores are part of words

        # 5. Handle strikethrough
        text = re.sub(r'~~(.*?)~~', r'\1', text)

        # 6. Handle images and links
        # ![alt text](url) -> alt text
        text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
        # [link text](url) -> link text
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)

        # 7. Handle horizontal rules
        text = re.sub(r'^\s*([-*_]){3,}\s*$', '', text, flags=re.MULTILINE)

        # 8. Handle blockquotes (remove >)
        text = re.sub(r'^\s*>\s?', '', text, flags=re.MULTILINE)

        # 9. Handle list items (remove *, -, + and numbers like 1.)
        # Unordered lists
        text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)
        # Ordered lists
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

        # Your existing replacements (adjust if needed after above changes)
        # text = text.replace('*', ' star ') # May no longer be needed if asterisks are stripped
        # text = text.replace('#', ' section ') # May no longer be needed if # are stripped

        # Remove excessive whitespace that might have been left after replacements
        text = re.sub(r'\s+', ' ', text).strip()
        # Ensure sentences still have good spacing.
        text = re.sub(r'\s*\.\s*', '. ', text) # Space after period
        text = re.sub(r'\s*,\s*', ', ', text) # Space after comma
        text = re.sub(r'\s*!\s*', '! ', text) # Space after exclamation
        text = re.sub(r'\s*\?\s*', '? ', text) # Space after question mark
        logging.info("Preprocessing complete.")
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Replace special characters that might affect speech
        text = text.replace('*', ' star ')
        text = text.replace('#', ' section ')
        # Clean up any remaining markdown-like syntax
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Remove links but keep link text
        return text

    def split_into_chunks(self, text, max_chars=5000):
        """Split text into manageable chunks for TTS processing"""
        # First, split by sentences
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chars:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:  # Add the last chunk if it exists
            chunks.append(current_chunk.strip())
            
        logging.info(f"Split text into {len(chunks)} chunks")
        return chunks

    def add_markup(self, text):
        """Add markup for emphasis and pauses"""
        # Make a copy of the text for modification
        marked_text = text
        
        # Mark text for emphasis - using safe substitution to avoid regex errors
        for pattern in self.emphasis_patterns:
            try:
                # Check if the pattern has capture groups
                if '(' in pattern and ')' in pattern:
                    # Use regex with capture groups
                    matches = re.finditer(pattern, marked_text)
                    # Process matches from end to start to avoid messing up positions
                    matches = list(matches)
                    for match in reversed(matches):
                        try:
                            # Get the captured group if it exists
                            if match.groups():
                                emphasis_text = match.group(1)
                                start, end = match.span(1)  # Get position of first capture group
                                marked_text = marked_text[:start] + "<emphasis>" + emphasis_text + "</emphasis>" + marked_text[end:]
                            else:
                                # If no capture group, emphasize the whole match
                                emphasis_text = match.group(0)
                                start, end = match.span(0)
                                marked_text = marked_text[:start] + "<emphasis>" + emphasis_text + "</emphasis>" + marked_text[end:]
                        except Exception as e:
                            logging.warning(f"Error processing emphasis match: {e}")
                else:
                    # Simple pattern without capture groups
                    matches = re.finditer(pattern, marked_text)
                    matches = list(matches)
                    for match in reversed(matches):
                        emphasis_text = match.group(0)
                        start, end = match.span(0)
                        marked_text = marked_text[:start] + "<emphasis>" + emphasis_text + "</emphasis>" + marked_text[end:]
            except Exception as e:
                logging.warning(f"Error applying emphasis pattern '{pattern}': {e}")
                continue
        
        # Mark positions for pauses - using safe substitution
        for pattern in self.pause_patterns:
            try:
                marked_text = re.sub(pattern, r'\g<0><pause></pause>', marked_text)
            except Exception as e:
                logging.warning(f"Error applying pause pattern '{pattern}': {e}")
                continue
                
        return marked_text

    def speak_with_effects(self, text, speed='normal'):
        """Speak text with appropriate pauses and emphasis"""
        try:
            # Set the speech rate
            self.engine.setProperty('rate', self.reading_speeds[speed])
            
            # Parse the text to find pause and emphasis markers
            segments = []
            current_pos = 0
            
            # Find all markers (both pause and emphasis)
            pause_markers = [(m.start(), m.end(), 'pause') for m in re.finditer(r'<pause></pause>', text)]
            emphasis_markers = [(m.start(), m.end(), 'emphasis_start') for m in re.finditer(r'<emphasis>', text)]
            emphasis_end_markers = [(m.start(), m.end(), 'emphasis_end') for m in re.finditer(r'</emphasis>', text)]
            
            # Combine all markers and sort by position
            all_markers = pause_markers + emphasis_markers + emphasis_end_markers
            all_markers.sort(key=lambda x: x[0])
            
            # Process text according to markers
            for start, end, marker_type in all_markers:
                if marker_type == 'pause':
                    # Extract text before pause
                    segment_text = text[current_pos:start]
                    # Remove any emphasis tags
                    segment_text = re.sub(r'<emphasis>|</emphasis>', '', segment_text)
                    segments.append((segment_text, False))
                    segments.append((None, 'pause'))  # Pause marker
                    current_pos = end
                elif marker_type == 'emphasis_start':
                    # Extract text before emphasis
                    if start > current_pos:
                        segment_text = text[current_pos:start]
                        segment_text = re.sub(r'<emphasis>|</emphasis>', '', segment_text)
                        segments.append((segment_text, False))
                    current_pos = end
                elif marker_type == 'emphasis_end':
                    # Extract emphasized text
                    segment_text = text[current_pos:start]
                    segment_text = re.sub(r'<emphasis>|</emphasis>', '', segment_text)

                    segments.append((segment_text, True))  # Emphasized text
                    current_pos = end
            
            # Add any remaining text
            if current_pos < len(text):
                segment_text = text[current_pos:]
                segment_text = re.sub(r'<emphasis>|</emphasis>', '', segment_text)
                segments.append((segment_text, False))
            
            # Process all segments
            for segment, effect in segments:
                if segment is None and effect == 'pause':
                    # Insert a pause
                    time.sleep(self.pause_durations['short'])
                elif segment:
                    # Skip empty segments
                    if not segment.strip():
                        continue
                        
                    if effect is True:  # Emphasized text
                        # Temporarily increase volume for emphasis
                        current_volume = self.engine.getProperty('volume')
                        self.engine.setProperty('volume', min(current_volume * 1.2, 1.0))
                        
                        # Speak the emphasized text
                        self.engine.say(segment)
                        self.engine.runAndWait()
                        
                        # Restore original volume
                        self.engine.setProperty('volume', current_volume)
                    else:
                        # Speak normal text
                        self.engine.say(segment)
                        self.engine.runAndWait()
                        
        except Exception as e:
            logging.error(f"Error in speak_with_effects: {e}")
            if self.status_var:
                self.status_var.set(f"Error: {e}")

    def run_cli(self):
        """Run the application in command-line interface mode"""
        print("=== Smart Educational Text Reader (CLI Mode) ===")
        
        # Show available voices
        print("\nAvailable voices:")
        for i, voice in enumerate(self.voices):
            print(f"{i+1}. {voice.name}")
        
        # Select voice
        try:
            voice_choice = int(input("\nSelect voice (enter number): ")) - 1
            if 0 <= voice_choice < len(self.voices):
                self.change_voice(voice_choice)
                print(f"Voice set to: {self.voices[voice_choice].name}")
            else:
                print("Invalid choice. Using default voice.")
        except ValueError:
            print("Invalid input. Using default voice.")
        
        # Select speed
        print("\nReading speeds: 1. Slow, 2. Normal, 3. Fast")
        try:
            speed_choice = int(input("Select speed (enter number): "))
            speed_options = list(self.reading_speeds.keys())
            if 1 <= speed_choice <= len(speed_options):
                selected_speed = speed_options[speed_choice-1]
                self.change_speed(selected_speed)
                print(f"Speed set to: {selected_speed}")
            else:
                print("Invalid choice. Using normal speed.")
        except ValueError:
            print("Invalid input. Using normal speed.")
        
        # Get file path
        file_path = input("\nEnter path to PDF or text file: ")
        
        # Process file
        text = None
        if file_path.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith(('.txt', '.md')):
            text = self.read_text_file(file_path)
        else:
            print("Unsupported file format. Please use PDF or TXT/MD files.")
            return
            
        if not text:
            print("Failed to extract text from the file.")
            return
        
        # Preprocess text
        self.preprocess_and_split_text(text)
        
        # Ask if user wants to save as audio
        save_audio = input("\nDo you want to save this as an audio file? (y/n): ").lower().startswith('y')
        
        if save_audio:
            file_path = input("Enter the path to save audio file (e.g., output.mp3): ")
            if file_path:
                self.save_audio_to_file(text, file_path)
        else:
            # Read text
            print("\nReading text. Press Ctrl+C to stop.")
            try:
                self.is_reading = True
                self.current_sentence_index = 0
                
                while self.current_sentence_index < len(self.sentences) and self.is_reading:
                    current = self.sentences[self.current_sentence_index]
                    print(f"\nReading: {current}")
                    
                    # Add markup for emphasis and pauses
                    marked_text = self.add_markup(current)
                    
                    # Read the text
                    self.speak_with_effects(marked_text, self.current_speed)
                    
                    # Move to next sentence
                    self.current_sentence_index += 1
                
                print("\nReading completed.")
                
            except KeyboardInterrupt:
                print("\nReading stopped by user.")
                self.engine.stop()
                self.is_reading = False


def main():
    """Main function to run the application"""
    # Check if running in GUI or CLI mode
    use_gui = True
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1].lower() == '--cli':
        use_gui = False
    
    if use_gui:
        try:
            # Initialize GUI
            root = tk.Tk()
            app = SmartReader(root)
            app.setup_gui()
            root.mainloop()
        except Exception as e:
            logging.error(f"Error running GUI: {e}")
            print(f"Error running GUI: {e}")
            print("Falling back to CLI mode...")
            app = SmartReader()
            app.run_cli()
    else:
        # Run in CLI mode
        app = SmartReader()
        app.run_cli()


if __name__ == "__main__":
    import sys
    main()