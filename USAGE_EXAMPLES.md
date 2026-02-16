# CV Creator - Usage Examples

This document provides examples of how to use the CV Creator application.

## Example 1: Running the Interactive Application

```bash
python3 cv_creator.py
```

You'll be guided through these steps:

### Step 1: Personal Information
```
============================================================
  Personal Information
============================================================

Full Name: John Smith
Email: john.smith@email.com
Phone: +1-234-567-8900
Location (City, Country): Boston, MA, USA
LinkedIn Profile (optional): linkedin.com/in/johnsmith
GitHub Profile (optional): github.com/johnsmith
Professional Summary (brief description): Software Engineer with 5 years of experience in web development
```

### Step 2: Education
```
============================================================
  Education
============================================================

Add Education Entry
----------------------------------------
Degree (e.g., Bachelor of Science): Bachelor of Science
Field of Study: Computer Science
Institution/University: MIT
Location: Cambridge, MA
Start Date (e.g., Sept 2018): Sept 2014
End Date (or 'Present'): May 2018
GPA (optional): 3.8
Key Achievements (optional): Summa Cum Laude

Add another education entry? (y/n): n
```

### Step 3: Work Experience
```
============================================================
  Work Experience
============================================================

Add Work Experience Entry
----------------------------------------
Job Title: Senior Software Engineer
Company Name: Tech Corp
Location: Boston, MA
Start Date (e.g., Jan 2020): June 2018
End Date (or 'Present'): Present

Job Responsibilities (enter one per line, empty line to finish):
- Led development of microservices architecture
- Mentored team of 5 junior developers
- Improved system performance by 40%
- 

Add another work experience? (y/n): n
```

### Step 4: Skills
```
============================================================
  Skills
============================================================

Enter your skills (comma-separated):
Example: Python, Machine Learning, Data Analysis, TensorFlow
Skills: Python, JavaScript, React, Node.js, Docker, Kubernetes, AWS
```

### Step 5: Optional Sections
```
Would you like to add languages? (y/n): y

============================================================
  Languages
============================================================

Add Language
----------------------------------------
Language: English
Proficiency (e.g., Native, Fluent, Intermediate): Native

Add another language? (y/n): n

Would you like to add certifications? (y/n): y

============================================================
  Certifications
============================================================

Add Certification
----------------------------------------
Certification Name: AWS Certified Solutions Architect
Issuing Organization: Amazon Web Services
Date Obtained: March 2022
Credential ID (optional): AWS-SAA-12345

Add another certification? (y/n): n
```

### Step 6: Preview and Save
```
============================================================
  CV PREVIEW
============================================================

[Your formatted CV is displayed here]

Press Enter to continue...

============================================================
  Save Your CV
============================================================

Enter filename prefix (default: my_cv): john_smith_cv

✓ CV data saved as: john_smith_cv_20240216_120000.json
✓ CV document saved as: john_smith_cv_20240216_120000.txt

============================================================
  CV Creation Complete!
============================================================

Your CV has been saved in two formats:
  1. JSON format: john_smith_cv_20240216_120000.json (for easy editing)
  2. Text format: john_smith_cv_20240216_120000.txt (ready to use)

Thank you for using CV Creator!
============================================================
```

## Example 2: Running the Demo

To see a pre-filled example:

```bash
python3 demo_cv_creator.py
```

This will create a sample CV with demo data and show you what the output looks like.

## Example 3: Running Tests

To verify the application works correctly:

```bash
python3 test_cv_creator.py
```

This runs automated tests to ensure all functionality works as expected.

## Tips for Best Results

1. **Be Specific**: Provide detailed but concise descriptions
2. **Use Action Verbs**: Start responsibilities with strong verbs (Led, Developed, Implemented, Managed)
3. **Quantify Results**: Include metrics when possible (e.g., "Improved performance by 40%")
4. **Keep It Professional**: Use formal language and proper grammar
5. **Save Both Formats**: Keep the JSON for easy updates, use the text file for applications

## Editing Your CV Later

To update your CV after creation:

1. Open the `.json` file in any text editor
2. Edit the information you want to change
3. Save the file
4. Use the data in the JSON to create a new text version

Alternatively, run the application again with updated information.

## Converting to Other Formats

The text file can be easily converted:

- **Microsoft Word/Google Docs**: Copy and paste the text, then format as needed
- **PDF**: Use any text-to-PDF converter or print to PDF from your word processor
- **HTML**: Use the JSON data to populate an HTML template
- **LaTeX**: Use the structured JSON data with a LaTeX CV template

## Common Use Cases

### For Students
- Focus on education and academic projects
- Include relevant coursework and GPA if strong
- Highlight internships and part-time work

### For Professionals
- Emphasize work experience and achievements
- Include recent and relevant education
- Showcase industry certifications

### For Career Changes
- Highlight transferable skills
- Focus on relevant experience
- Include courses or certifications in new field

## Troubleshooting

### Application doesn't start
- Check Python version: `python3 --version` (requires 3.6+)
- Try: `python cv_creator.py` instead of `python3`

### Special characters not displaying
- Ensure your terminal supports UTF-8
- Use a modern text editor to view files

### Want to exit during creation
- Press `Ctrl+C` to cancel at any time
- No files will be saved if you exit early

## Getting Help

For more detailed information, see [CV_CREATOR_README.md](CV_CREATOR_README.md)
