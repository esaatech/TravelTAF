from django import forms

class CRSCalculatorForm(forms.Form):
    # Marital Status and Spouse Info
    marital_status = forms.ChoiceField(
        choices=[
            ('single', 'Single'),
            ('married', 'Married or Common-Law'),
        ],
        label="What is your marital status?"
    )

    spouse_canadian_status = forms.ChoiceField(
        required=False,
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
        ],
        label="Is your spouse/common-law partner a citizen or permanent resident of Canada?"
    )

    spouse_coming_to_canada = forms.ChoiceField(
        required=False,
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
        ],
        label="Will your spouse/common-law partner come with you to Canada?"
    )

    # Core Human Capital Factors
    age = forms.IntegerField(
        min_value=17,
        max_value=45,
        label="How old are you?"
    )

    education_level = forms.ChoiceField(
        choices=[
            (0, "Less than secondary school"),
            (28, "Secondary diploma (high school)"),
            (84, "One-year post-secondary program"),
            (91, "Two-year post-secondary program"),
            (112, "Bachelor's degree (three or more years)"),
            (119, "Two or more post-secondary programs (one 3+ years)"),
            (126, "Master's degree"),
            (140, "Doctoral degree (Ph.D.)")
        ],
        label="What is your level of education?"
    )

    canadian_education = forms.ChoiceField(
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
        ],
        label="Have you earned a Canadian degree, diploma or certificate?"
    )

    # Language Skills
    language_test_type = forms.ChoiceField(
        choices=[
            ('ielts', 'IELTS'),
            ('celpip', 'CELPIP'),
            ('tef', 'TEF Canada'),
            ('tcf', 'TCF Canada')
        ],
        label="Which language test did you take?"
    )

    speaking = forms.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=9,
        label="Speaking Score"
    )

    listening = forms.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=9,
        label="Listening Score"
    )

    reading = forms.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=9,
        label="Reading Score"
    )

    writing = forms.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=9,
        label="Writing Score"
    )

    # Work Experience
    canadian_work_experience = forms.ChoiceField(
        choices=[
            (0, 'None'),
            (35, '1 year'),
            (46, '2 years'),
            (56, '3 years'),
            (63, '4 years'),
            (70, '5 years or more')
        ],
        label="Canadian Work Experience"
    )

    foreign_work_experience = forms.ChoiceField(
        choices=[
            (0, 'None'),
            (13, '1-2 years'),
            (25, '3 years or more')
        ],
        label="Foreign Work Experience"
    )

    # Additional Points
    certificate_qualification = forms.BooleanField(
        required=False,
        label="Do you have a certificate of qualification from a Canadian province/territory?"
    )

    job_offer = forms.ChoiceField(
        choices=[
            (0, 'No job offer'),
            (200, 'Senior executive role (NOC 00)'),
            (50, 'NOC TEER 1, 2, 3, or other TEER 0')
        ],
        label="Valid Job Offer"
    )

    provincial_nomination = forms.BooleanField(
        required=False,
        label="Do you have a provincial nomination?"
    )

    canadian_sibling = forms.BooleanField(
        required=False,
        label="Do you have a sibling who is a Canadian citizen/permanent resident?"
    )

    # Spouse Factors (if applicable)
    spouse_education = forms.ChoiceField(
        required=False,
        choices=[
            (0, "Less than secondary school"),
            (2, "Secondary diploma"),
            (6, "One-year post-secondary"),
            (7, "Two-year post-secondary"),
            (8, "Bachelor's degree"),
            (9, "Two or more post-secondary degrees"),
            (10, "Master's or Doctoral degree")
        ],
        label="Spouse's Education Level"
    )

    spouse_work_experience = forms.ChoiceField(
        required=False,
        choices=[
            (0, 'None'),
            (5, '1-2 years'),
            (7, '3-4 years'),
            (8, '5+ years')
        ],
        label="Spouse's Canadian Work Experience"
    )

    # Spouse Language Skills
    spouse_language_test = forms.ChoiceField(
        required=False,
        choices=[
            ('none', 'No Test'),
            ('ielts', 'IELTS'),
            ('celpip', 'CELPIP'),
            ('tef', 'TEF Canada'),
            ('tcf', 'TCF Canada')
        ],
        label="Spouse's Language Test"
    )

    spouse_speaking = forms.DecimalField(
        required=False,
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=9,
        label="Spouse Speaking Score"
    )

    spouse_listening = forms.DecimalField(
        required=False,
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=9,
        label="Spouse Listening Score"
    )

    spouse_reading = forms.DecimalField(
        required=False,
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=9,
        label="Spouse Reading Score"
    )

    spouse_writing = forms.DecimalField(
        required=False,
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=9,
        label="Spouse Writing Score"
    )