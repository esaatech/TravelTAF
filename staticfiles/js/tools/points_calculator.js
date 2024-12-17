/**
 * CRS (Comprehensive Ranking System) Points Calculator
 * 
 * A comprehensive tool for calculating immigration points based on various factors:
 * 1. Core/Human Capital Factors (max 500 points)
 * 2. Spouse Factors (max 40 points)
 * 3. Skill Transferability (max 100 points)
 * 4. Additional Points (max 600 points)
 * 
 * Required DOM Elements:
 * #crsCalculator - Main calculator form
 * #results - Results display container
 * #totalScore - Total score display
 * #corePoints - Core points display
 * #spousePoints - Spouse points display
 * #skillPoints - Skill points display
 * #additionalPoints - Additional points display
 * 
 * Score Calculation Functions:
 * 
 * calculateScore(data)
 * - Main calculation function
 * - Processes all point categories
 * - Combines scores for final result
 * 
 * calculateAgePoints(age)
 * - Age points (17-45 years)
 * - Returns 0-110 points based on age
 * 
 * calculateLanguagePoints(data)
 * - Language proficiency points
 * - CLB levels for speaking, listening, reading, writing
 * - Returns 0-128 points
 * 
 * calculateSpouseLanguagePoints(data)
 * - Spouse language points
 * - Similar to primary applicant but lower scale
 * - Returns 0-20 points
 * 
 * calculateSkillTransferability(data)
 * - Education + Language combination
 * - Education + Experience combination
 * - Foreign Work + Language combination
 * - Max 100 points
 * 
 * calculateAdditionalPoints(data)
 * - Provincial nomination (600 points)
 * - Job offer (50-200 points)
 * - Canadian education (15-30 points)
 * - Sibling in Canada (15 points)
 * 
 * Validation:
 * - Required fields
 * - Age range (17-45)
 * - Language scores (0-9)
 * - Education levels
 * - Work experience
 * 
 * Error Handling:
 * - Field validation
 * - Visual error indicators
 * - Error messages display
 * - Automatic error clearing
 * 
 * UI Features:
 * - Real-time validation
 * - Error highlighting
 * - Smooth scrolling to results/errors
 * - Clear error messages
 * 
 * Score Categories:
 * 1. Core Points (max 500)
 *    - Age
 *    - Education
 *    - Language skills
 *    - Canadian work experience
 * 
 * 2. Spouse Points (max 40)
 *    - Education
 *    - Language skills
 *    - Work experience
 * 
 * 3. Skill Transferability (max 100)
 *    - Education + Language
 *    - Education + Experience
 *    - Foreign Work + Language
 * 
 * 4. Additional Points (max 600)
 *    - Provincial nomination
 *    - Job offer
 *    - Canadian education
 *    - Sibling in Canada
 * 
 * Dependencies:
 * - Modern browser with ES6+ support
 * - DOM manipulation capabilities
 * - FormData API support
 * 
 * Usage:
 * - Fill out the form with applicant details
 * - Submit for immediate calculation
 * - View breakdown of points by category
 * - Review any validation errors
 * 
 * Error Display:
 * - Red border on error fields
 * - Error messages at top of form
 * - Automatic scroll to errors
 * - Clear indication of required fixes
 */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('crsCalculator');
    const results = document.getElementById('results');

    // Form submission handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Clear previous errors
        clearErrors();
        
        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Validate form
        const errors = validateForm(data);
        
        if (errors.length > 0) {
            showErrors(errors);
            return;
        }

        // If validation passes, calculate score
        calculateScore(data);
    });

    function calculateScore(data) {
        // Initialize scores
        let corePoints = 0;
        let spousePoints = 0;
        let skillPoints = 0;
        let additionalPoints = 0;

        // 1. Core/Human Capital Factors (max 500 points)
        corePoints += calculateAgePoints(parseInt(data.age));
        corePoints += parseInt(data.education_level);
        corePoints += calculateLanguagePoints(data);
        corePoints += parseInt(data.canadian_work_experience);

        // 2. Spouse Factors (max 40 points)
        if (data.marital_status === 'married' && data.spouse_coming_to_canada === 'yes') {
            spousePoints += parseInt(data.spouse_education) || 0;
            spousePoints += calculateSpouseLanguagePoints(data);
            spousePoints += parseInt(data.spouse_work_experience) || 0;
        }

        // 3. Skill Transferability (max 100 points)
        skillPoints += calculateSkillTransferability(data);

        // 4. Additional Points (max 600 points)
        additionalPoints += calculateAdditionalPoints(data);

        // Display results
        displayResults(corePoints, spousePoints, skillPoints, additionalPoints);
    }

    function calculateAgePoints(age) {
        if (age < 18) return 0;
        if (age > 45) return 0;

        const agePoints = {
            18: 99, 19: 105, 20: 110, 21: 110, 22: 110, 23: 110, 24: 110,
            25: 110, 26: 110, 27: 110, 28: 110, 29: 110, 30: 110, 31: 109,
            32: 105, 33: 99, 34: 94, 35: 88, 36: 82, 37: 77, 38: 71,
            39: 65, 40: 59, 41: 53, 42: 47, 43: 41, 44: 35, 45: 29
        };

        return agePoints[age] || 0;
    }

    function calculateLanguagePoints(data) {
        let points = 0;
        const fields = ['speaking', 'listening', 'reading', 'writing'];
        
        fields.forEach(field => {
            const score = parseFloat(data[field]);
            if (score >= 7) points += 32;
            else if (score >= 6) points += 23;
            else if (score >= 5) points += 16;
            else if (score >= 4) points += 6;
        });

        return points;
    }

    function calculateSpouseLanguagePoints(data) {
        let points = 0;
        const fields = ['spouse_speaking', 'spouse_listening', 'spouse_reading', 'spouse_writing'];
        
        fields.forEach(field => {
            const score = parseFloat(data[field]);
            if (score >= 7) points += 5;
            else if (score >= 6) points += 3;
            else if (score >= 5) points += 1;
        });

        return points;
    }

    function calculateSkillTransferability(data) {
        let points = 0;
        const education = parseInt(data.education_level);
        const language = calculateLanguagePoints(data);
        const foreignExp = parseInt(data.foreign_work_experience);
        const canadianExp = parseInt(data.canadian_work_experience);

        // Education + Language
        if (education >= 112 && language >= 128) points += 50;
        else if (education >= 112 && language >= 92) points += 25;

        // Education + Experience
        if (education >= 112 && foreignExp >= 3) points += 50;
        else if (education >= 112 && foreignExp >= 1) points += 25;

        // Foreign Work + Language
        if (foreignExp >= 3 && language >= 128) points += 50;
        else if (foreignExp >= 1 && language >= 92) points += 25;

        return Math.min(100, points); // Cap at 100 points
    }

    function calculateAdditionalPoints(data) {
        let points = 0;

        // Provincial nomination
        if (data.provincial_nomination === 'true') points += 600;

        // Job offer
        points += parseInt(data.job_offer) || 0;

        // Canadian education
        if (data.canadian_education === 'yes') {
            const educationLevel = parseInt(data.education_level);
            if (educationLevel >= 112) points += 30;
            else points += 15;
        }

        // Sibling in Canada
        if (data.canadian_sibling === 'true') points += 15;

        return points;
    }

    function displayResults(core, spouse, skill, additional) {
        const total = core + spouse + skill + additional;
        
        // Show results section
        results.classList.remove('hidden');
        
        // Update score displays
        document.getElementById('totalScore').textContent = total;
        document.getElementById('corePoints').textContent = core;
        document.getElementById('spousePoints').textContent = spouse;
        document.getElementById('skillPoints').textContent = skill;
        document.getElementById('additionalPoints').textContent = additional;
        
        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth' });
    }

    // Validation functions
    function clearErrors() {
        const existingErrors = document.getElementById('error-container');
        if (existingErrors) {
            existingErrors.remove();
        }
        form.querySelectorAll('.error-field').forEach(field => {
            field.classList.remove('error-field', 'border-red-500', 'bg-red-50');
        });
    }

    function validateForm(data) {
        const errors = [];

        // Required fields validation
        const requiredFields = {
            age: 'Age',
            education_level: 'Education Level',
            speaking: 'Speaking Score',
            listening: 'Listening Score',
            reading: 'Reading Score',
            writing: 'Writing Score',
            canadian_work_experience: 'Canadian Work Experience',
            foreign_work_experience: 'Foreign Work Experience'
        };

        Object.entries(requiredFields).forEach(([field, label]) => {
            if (!data[field] || data[field].trim() === '') {
                errors.push(`${label} is required`);
                highlightErrorField(field);
            }
        });

        // Age range validation
        if (data.age) {
            const age = parseInt(data.age);
            if (age < 17 || age > 45) {
                errors.push('Age must be between 17 and 45');
                highlightErrorField('age');
            }
        }

        // Language scores validation
        const languageFields = ['speaking', 'listening', 'reading', 'writing'];
        languageFields.forEach(field => {
            if (data[field]) {
                const score = parseFloat(data[field]);
                if (score < 0 || score > 9) {
                    errors.push(`${field.charAt(0).toUpperCase() + field.slice(1)} score must be between 0 and 9`);
                    highlightErrorField(field);
                }
            }
        });

        return errors;
    }

    function highlightErrorField(fieldName) {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (field) {
            field.classList.add('error-field', 'border-red-500', 'bg-red-50');
        }
    }

    function showErrors(errors) {
        const errorContainer = document.createElement('div');
        errorContainer.id = 'error-container';
        errorContainer.className = 'bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded';
        
        const errorHeader = document.createElement('h3');
        errorHeader.className = 'text-red-700 font-bold mb-2';
        errorHeader.textContent = 'Please correct the following errors:';
        errorContainer.appendChild(errorHeader);
        
        const errorList = document.createElement('ul');
        errorList.className = 'text-red-700 list-disc list-inside';
        errors.forEach(error => {
            const li = document.createElement('li');
            li.className = 'text-sm';
            li.textContent = error;
            errorList.appendChild(li);
        });
        errorContainer.appendChild(errorList);
        
        form.insertBefore(errorContainer, form.firstChild);
        errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}); 