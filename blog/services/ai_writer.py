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

    def generate_introduction(self, topic, category=None, tone="informative", context=None):
        try:
            base_prompt = """You are an SEO-optimized blog writing assistant that creates engaging, structured, and reader-friendly introductions for blog posts.
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
            """

            # Add context if provided
            if context:
                base_prompt += """
                
                Please use the following context as a foundation for the introduction:
                {context}
                
                Important:
                - Maintain factual accuracy from the context
                - Expand upon the ideas presented
                - Keep the engaging tone while incorporating key points
                """

            prompt = base_prompt.format(
                topic=topic, 
                category=category, 
                tone=tone,
                context=context
            )

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional blog writer for a travel and immigration website. Output content in HTML format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7 if not context else 0.5  # Lower temperature when using context for more accuracy
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating introduction: {str(e)}")
            raise

    def generate_body(self, topic, introduction, category=None, tone="informative", context=None):
        try:
            base_prompt = """You are an SEO-optimized blog writing assistant that creates structured, informative, and engaging blog post that keep readers interested and provide clear, actionable insights.
            
            Topic: {topic}
            Introduction: {introduction}
            Tone: {tone}
            
            Guidelines:
            1. Use proper HTML heading tags (<h2> and <h3>) for structure
            2. Support claims with data and examples
            3. Use <p> tags for paragraphs
            4. Use <ul> and <li> for bullet points
            5. End with a strong Call-to-Action (CTA)
            6. Keep paragraphs short (4-6 sentences)
            7. Ensure a natural, conversational tone
            8. Provide data and examples where relevant
            """

            # Add context if provided
            if context:
                base_prompt += """
                
                Please use the following context as a foundation for the content:
                {context}
                
                Important:
                - Use the provided context as the primary source of information
                - Maintain factual accuracy from the context
                - Expand upon the ideas while staying true to the source
                - Add relevant examples and explanations
                - Structure the content logically
                """

            prompt = base_prompt.format(
                topic=topic,
                introduction=introduction,
                category=category,
                tone=tone,
                context=context
            )

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a factual travel database assistant. Your task is to provide precise, comprehensive, and structured responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5 if context else 0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating body: {str(e)}")
            raise

    def generate_post(self, topic, category=None, tone="informative", context=None):
        try:
            logger.info(f"Generating post for topic: {topic}, category: {category}, tone: {tone}")
            
            # Step 1: Generate Introduction
            introduction = self.generate_introduction(topic, category, tone, context)
            logger.info("Introduction generated successfully")
            
            # Step 2: Generate Body
            body = self.generate_body(topic, introduction, category, tone, context)
            logger.info("Body generated successfully")
            
            # Combine content
            full_content = f"{introduction}\n\n{body}"
            
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
    """ 
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

    """
    # Without context (original behavior)
    post = writer.generate_post("Visa Requirements for Canada")
    print("\nFull Post without context :..................................................")
    print(post['content'])
    # With context
    context = """
    Canada's visitor visa requirements vary by country. Most visitors need:
    1. Valid passport
    2. Proof of funds
    3. Purpose of travel
    4. Clean criminal record
    Processing time: 14-30 days
    Cost: CAD$100
    """
    post = writer.generate_post(
        topic="Visa Requirements for Canada",
        category="Immigration",
        tone="informative",
        context=context
    ) 
    print("\nFull Post:..................................................")
    print(post['content'])