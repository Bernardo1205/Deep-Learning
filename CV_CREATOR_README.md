# CV Creator Application

A simple and user-friendly command-line application to help you create your own professional CV (Curriculum Vitae).

## Features

- **Interactive Step-by-Step Process**: Guides you through each section of your CV
- **Comprehensive Sections**:
  - Personal Information (name, contact details, social profiles)
  - Professional Summary
  - Education (multiple entries supported)
  - Work Experience (with detailed responsibilities)
  - Skills
  - Languages (optional)
  - Certifications (optional)
- **Multiple Output Formats**:
  - JSON format (for easy editing and future updates)
  - Formatted text document (ready to use)
- **Preview Before Saving**: Review your CV before finalizing
- **No External Dependencies**: Uses only Python standard library

## Requirements

- Python 3.6 or higher

## How to Use

### Basic Usage

1. Make the script executable (optional):
   ```bash
   chmod +x cv_creator.py
   ```

2. Run the application:
   ```bash
   python3 cv_creator.py
   ```
   or if you made it executable:
   ```bash
   ./cv_creator.py
   ```

3. Follow the interactive prompts to enter your information

4. Review the preview of your CV

5. Save your CV with your preferred filename

### Step-by-Step Guide

1. **Personal Information**: Enter your basic contact details and professional summary

2. **Education**: Add one or more educational qualifications
   - You can add multiple degrees
   - Include GPA and achievements if desired

3. **Work Experience**: Add your work history
   - Add multiple positions
   - List responsibilities for each role
   - Include dates and locations

4. **Skills**: List your technical and professional skills
   - Enter as comma-separated values
   - Example: Python, Machine Learning, Data Analysis

5. **Languages** (Optional): Add languages you speak and proficiency levels

6. **Certifications** (Optional): Add professional certifications with details

7. **Preview & Save**: Review your CV and save in multiple formats

## Output Files

The application generates two files:

1. **JSON File** (`my_cv_YYYYMMDD_HHMMSS.json`):
   - Contains all your CV data in structured format
   - Easy to edit and update later
   - Can be used with other applications

2. **Text File** (`my_cv_YYYYMMDD_HHMMSS.txt`):
   - Professionally formatted CV document
   - Ready to copy to word processors
   - Easy to read and share

## Example Output

```
================================================================================
JOHN DOE
================================================================================
Email: john.doe@email.com | Phone: +1-234-567-8900
Location: New York, USA
LinkedIn: linkedin.com/in/johndoe
GitHub: github.com/johndoe

--------------------------------------------------------------------------------
PROFESSIONAL SUMMARY
--------------------------------------------------------------------------------
Experienced software engineer with 5+ years in full-stack development...

--------------------------------------------------------------------------------
EDUCATION
--------------------------------------------------------------------------------

Bachelor of Science in Computer Science
MIT, Cambridge, MA
Sept 2015 - May 2019
GPA: 3.8/4.0

--------------------------------------------------------------------------------
WORK EXPERIENCE
--------------------------------------------------------------------------------

Senior Software Engineer
Tech Company, San Francisco, CA
Jan 2020 - Present
Responsibilities:
  • Led development of microservices architecture
  • Mentored junior developers
  • Implemented CI/CD pipelines

...
```

## Tips for Best Results

1. **Be Concise**: Keep descriptions clear and to the point
2. **Use Action Verbs**: Start responsibilities with strong action verbs (Led, Developed, Implemented)
3. **Quantify Achievements**: Include numbers and metrics when possible
4. **Keep Updated**: Save the JSON file to easily update your CV later
5. **Proofread**: Review the preview carefully before saving

## Customization

The generated text file can be:
- Copied to Microsoft Word, Google Docs, or other word processors
- Further formatted with fonts, colors, and styling
- Converted to PDF for professional submissions
- Edited directly for quick updates

## Troubleshooting

### Application doesn't start
- Ensure Python 3.6+ is installed: `python3 --version`
- Check file permissions if using `./cv_creator.py`

### Special characters not displaying
- Use UTF-8 compatible text editors to view output files
- The application automatically handles Unicode characters

### Want to edit your CV later
- Keep the JSON file and modify it in any text editor
- Re-run the application and paste updated information

## Future Enhancements

Potential additions to the application:
- PDF generation support
- HTML/web format output
- Template selection
- Import from existing CV files
- GUI interface
- LaTeX format export

## License

This application is provided as-is for personal and professional use.

## Support

For issues or questions, please refer to the repository documentation or create an issue in the repository.

---

**Happy CV Creating!** 🎉
