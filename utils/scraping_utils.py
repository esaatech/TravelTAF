from bs4 import BeautifulSoup
import requests

class NewsScraperService:
    def scrape_and_structure(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        structured_content = []
        
        # Example structure for scraped content
        for element in soup.find_all(['p', 'table', 'ul', 'blockquote', 'img']):
            if element.name == 'p':
                structured_content.append({
                    'type': 'paragraph',
                    'content': element.text.strip()
                })
            elif element.name == 'table':
                structured_content.append({
                    'type': 'table',
                    'headers': [th.text for th in element.find_all('th')],
                    'rows': [[td.text for td in row.find_all('td')] 
                            for row in element.find_all('tr')[1:]]
                })
            # Add more element types as needed
        
        return structured_content
