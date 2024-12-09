from openai import OpenAI
from datetime import datetime

# Initialize the client
client = OpenAI()  # Make sure OPENAI_API_KEY is set in your environment



def generate_cover_letter_from_raw_text(job_posting, resume_text):
    """
    Generate a cover letter from raw job posting and resume text.
    The LLM will first analyze and extract relevant information, then create the cover letter.
    """
    analysis_prompt = f"""
    First, analyze the following job posting and resume to extract relevant information:

    JOB POSTING:
    {job_posting}

    RESUME:
    {resume_text}

    Please analyze both texts and extract:
    1. From the job posting:
        - Position title
        - Company name
        - Key requirements
        - Department/team (if mentioned)
        - Required skills
        - Company values or culture indicators
    
    2. From the resume:
        - Candidate's name
        - Current role
        - Relevant experience matching job requirements
        - Key achievements that align with the position
        - Skills that match the job requirements
        
    3. Identify the top 3 most relevant experiences/skills from the resume that match the job requirements.
    
    Format your analysis as a structured summary.
    """

    try:
        # First, analyze the input texts
        analysis = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing job postings and resumes to identify relevant matches and key information."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.5
        )

        # Use the analysis to generate the cover letter
        cover_letter_prompt = f"""
        Using the following analysis, create a compelling cover letter:

        {analysis.choices[0].message.content}

        The cover letter should:
        1. Be professionally formatted with proper header and date
        2. Focus on the most relevant experiences identified in the analysis
        3. Demonstrate clear understanding of the company's needs
        4. Show enthusiasm for the role and company
        5. Include specific examples and achievements
        6. Maintain a professional yet engaging tone
        7. End with a strong call to action

        Keep the length to one page maximum.
        """

        cover_letter = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer who creates compelling, tailored cover letters."},
                {"role": "user", "content": cover_letter_prompt}
            ],
            temperature=0.7
        )

        return {
            'success': True,
            'analysis': analysis.choices[0].message.content,
            'cover_letter': cover_letter.choices[0].message.content
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

















def generate_cover_letter(job_details, candidate_details):
    prompt = f"""
    Generate a professional cover letter with the following details:

    JOB DETAILS:
    - Position: {job_details['position']}
    - Company: {job_details['company']}
    - Job Description: {job_details['description']}
    - Department/Team: {job_details['department']}
    
    CANDIDATE DETAILS:
    - Name: {candidate_details['name']}
    - Current Role: {candidate_details['current_role']}
    - Years of Experience: {candidate_details['experience']}
    - Key Skills: {candidate_details['skills']}
    - Notable Achievements: {candidate_details['achievements']}
    
    FORMATTING REQUIREMENTS:
    1. Professional header with contact information
    2. Current date
    3. Recipient's information if provided
    4. Proper greeting
    5. Three main paragraphs:
       - Opening: Position interest and source
       - Body: Relevant experience and achievements
       - Closing: Company-specific interest and call to action
    6. Professional closing
    7. Maximum length: One page
    
    STYLE REQUIREMENTS:
    - Formal but engaging tone
    - Specific examples rather than generic statements
    - Company research incorporation
    - Clear value proposition
    - Action-oriented language
    - No clichés or overused phrases
    
    MUST INCLUDE:
    1. Specific mention of the role and company name
    2. Connection between candidate's experience and job requirements
    3. Measurable achievements when possible
    4. Knowledge of company's values or recent developments
    5. Clear call to action for next steps
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer specializing in creating compelling, tailored cover letters that highlight candidate strengths and align with specific job requirements."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"


if __name__ == "__main__":
    # Example usage:
    job_details = {
        "position": "Senior Software Engineer",
        "company": "Tech Corp",
        "description": "Looking for experienced developer...",
        "department": "Engineering"
    }

    candidate_details = {
        "name": "Jane Smith",
        "current_role": "Software Engineer",
        "experience": "5 years",
        "skills": "Python, JavaScript, AWS",
        "achievements": "Led team of 5, increased efficiency by 40%"
    }     

    #cover_letter = generate_cover_letter(job_details, candidate_details)       
    #print(cover_letter)

    
    # Example usage with raw text
    job_posting = """
    Senior Software Engineer - AI/ML Team
    
    We're looking for a Senior Software Engineer to join our AI/ML team. The ideal candidate will have strong Python experience and a background in machine learning deployments. You'll be responsible for building and maintaining our ML infrastructure and working closely with data scientists.

    Requirements:
    - 5+ years of software development experience
    - Strong Python programming skills
    - Experience with ML frameworks (TensorFlow, PyTorch)
    - Knowledge of cloud platforms (AWS preferred)
    - Experience with containerization and orchestration
    
    About us:
    Tech Corp is a leading AI company focused on building ethical AI solutions. We value innovation, collaboration, and continuous learning.
    """

    resume = """
    JANE SMITH
    Software Engineer
    email@example.com | (555) 123-4567

    EXPERIENCE
    Senior Developer, AI Solutions Inc.
    2020-Present
    - Led team of 5 developers in building ML pipeline
    - Reduced model deployment time by 40%
    - Implemented automated testing for ML models

    Software Engineer, Tech Startup
    2018-2020
    - Developed Python microservices
    - Worked with AWS and Docker

    SKILLS
    Python, TensorFlow, PyTorch, AWS, Docker, Kubernetes
    """

    result = generate_cover_letter_from_raw_text(job_posting, resume)
    
    if result['success']:
        print("ANALYSIS:")
        print("-" * 50)
        print(result['analysis'])
        print("\nCOVER LETTER:")
        print("-" * 50)
        print(result['cover_letter'])
    else:
        print("Error:", result['error'])
