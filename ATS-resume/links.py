with open('D:\dd', 'r') as file:
  lines = file.readlines()
  
links = []
for line in lines:
  # Extract the URL part after the colon
  if ':' in line:
    link = line.split(':', 1)[1].strip()
    links.append(link)

# Print the list of links
print(links)
