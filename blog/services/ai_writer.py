from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import markdown2  # You'll need to pip install markdown2

logger = logging.getLogger(__name__)

class AIBlogWriter:
    def __init__(self):
        try:
            # Reload environment variables every time
            load_dotenv(override=True)
            
            # Initialize OpenAI client with fresh API key
            self.client = OpenAI()
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise

    def _convert_markdown_to_html(self, markdown_content):
        try:
            # Replace H2 and H3 markers with proper markdown syntax
            content = markdown_content.replace('H2 ', '## ')
            content = content.replace('H3 ', '### ')
            
            # Convert Markdown to HTML with extras for better formatting
            html_content = markdown2.markdown(content, extras=[
                'break-on-newline',
                'tables',
                'header-ids',
                'fenced-code-blocks',
                'cuddled-lists',
                'markdown-in-html'
            ])
            
            # Convert to plain string to ensure database compatibility
            return str(html_content)
        except Exception as e:
            logger.error(f"Error converting markdown to HTML: {str(e)}")
            raise

    def generate_introduction(self, topic, category=None, tone="informative"):
        try:
            prompt = """You are an SEO-optimized blog writing assistant that creates engaging, structured, and reader-friendly introductions for blog posts.
            Your goal is to hook the reader, clearly state the topic, and set the right expectations while maintaining a positive and engaging tone.
            
            Create an introduction for a blog post about: {topic}
            Category: {category}
            Tone: {tone}
            
            Guidelines:
            1. Capture reader's attention with a relatable concern or engaging hook
            2. Clearly state the topic and what the post will cover
            3. Address common concerns or questions
            4. Set expectations for what they will learn
            5. End with a positive, motivating statement
            6. Keep it concise (3-5 sentences)
            7. Use natural, engaging tone matching the audience
            
            IMPORTANT: Format the output in HTML using <p> tags for paragraphs.
            """.format(topic=topic, category=category, tone=tone)

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional blog writer for a travel and immigration website. Output content in HTML format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating introduction: {str(e)}")
            raise

    def generate_body(self, topic, introduction, category=None, tone="informative"):
        try:
            prompt = """You are an SEO-optimized blog writing assistant that creates structured, informative, and engaging blog post that keep readers interested and provide clear, actionable insights. Your goal is to ensure that the content is well-organized, easy to read, and valuable to the target audience, using the title and introduction provided 
            
            
            Topic: {topic}
            Introduction: {introduction}
            Tone: {tone}
            
            
            1. Use proper HTML heading tags (<h2> and <h3>) for structure
            2. Support claims with data and examples
            3. Use <p> tags for paragraphs
            4. Use <ul> and <li> for bullet points
            5. End with a strong Call-to-Action (CTA) that encourages further engagement, such as comments, sign-ups, or additional reading.
            6. Keep paragraphs short (4-6 sentences)
            7. Ensure a natural, conversational tone to keep the writing engaging and easy to follow
            8.Maintain a conversational tone that makes the content engaging and relatable.
            9.Provide data, comparisons, or examples where relevant to support claims and make the content more trustworthy
            
            IMPORTANT: Format the entire output in HTML with proper tags:
            - Use <h2> for main sections
            - Use <h3> for subsections
            - Use <p> for paragraphs
            - Use <ul> and <li> for lists
            - Ensure all tags are properly closed
            
            Example format:
            <h2>Main Section</h2>
            <p>Paragraph content...</p>
            <h3>Subsection</h3>
            <p>More content...</p>
            <ul>
                <li>List item 1</li>
                <li>List item 2</li>
            </ul>
            """.format(topic=topic, introduction=introduction, category=category, tone=tone)

            response = self.client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a factual travel database assistant. Your task is to provide precise, comprehensive, and structured responses."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.5,
    max_tokens=2000  # Increase max token limit
)
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating body: {str(e)}")
            raise

    def generate_post(self, topic, category=None, tone="informative"):
        try:
            logger.info(f"Generating post for topic: {topic}, category: {category}, tone: {tone}")
            
            # Step 1: Generate Introduction
            introduction = self.generate_introduction(topic, category, tone)
            logger.info("Introduction generated successfully")
            
            # Step 2: Generate Body
            body = self.generate_body(topic, introduction, category, tone)
            logger.info("Body generated successfully")
            
            # Combine content (already in HTML format)
            full_content = f"{introduction}\n\n{body}"
            print(f"Full Content: {full_content}")
            
            return {
                'title': str(topic),
                'content': str(full_content)
            }
            
        except Exception as e:
            logger.error(f"Error generating post: {str(e)}")
            raise
       

if __name__ == "__main__":
    # Test the AI writer
    writer = AIBlogWriter()
    
    test_topic = "Countries You Can Visit Visa-Free with a US Visa in 2025"
    test_category = "Education"
    test_tone = "informative"
    
    try:
        print("\nTesting full post generation...")
        post = writer.generate_post(test_topic, test_category, test_tone)
        print("\nFull Post:")
        print(f"Title: {post['title']}")
        print("\nHTML Content:")
        print(post['content'])
        
    except Exception as e:
        print(f"Error during testing: {str(e)}") 