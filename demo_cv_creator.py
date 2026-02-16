#!/usr/bin/env python3
"""
Demo script for CV Creator Application
This demonstrates the CV creator with sample data in a non-interactive way
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cv_creator import CVCreator


def demo_cv_creator():
    """Demonstrate CV creator with sample data"""
    print("\n" + "=" * 70)
    print("  CV CREATOR - DEMO MODE")
    print("  Creating a sample CV to demonstrate the application")
    print("=" * 70)
    
    # Create instance
    creator = CVCreator()
    
    # Populate with demo data
    creator.cv_data['personal_info'] = {
        'full_name': 'Alex Johnson',
        'email': 'alex.johnson@example.com',
        'phone': '+1-555-987-6543',
        'location': 'Austin, Texas, USA',
        'linkedin': 'linkedin.com/in/alexjohnson',
        'github': 'github.com/alexjohnson',
        'summary': 'Passionate software developer with 3+ years of experience in building scalable web applications and cloud solutions. Proficient in Python, JavaScript, and DevOps practices.'
    }
    
    creator.cv_data['education'] = [
        {
            'degree': 'Bachelor of Science',
            'field': 'Computer Science',
            'institution': 'University of Texas at Austin',
            'location': 'Austin, TX',
            'start_date': 'Aug 2016',
            'end_date': 'May 2020',
            'gpa': '3.7/4.0',
            'achievements': 'Dean\'s Honor List, President of CS Club'
        }
    ]
    
    creator.cv_data['experience'] = [
        {
            'job_title': 'Full Stack Developer',
            'company': 'Tech Innovations LLC',
            'location': 'Austin, TX',
            'start_date': 'June 2020',
            'end_date': 'Present',
            'responsibilities': [
                'Developed RESTful APIs using Python Flask and FastAPI',
                'Built responsive front-end applications with React and TypeScript',
                'Implemented CI/CD pipelines using GitHub Actions and Docker',
                'Reduced application load time by 40% through performance optimization',
                'Collaborated with team of 8 developers using Agile methodologies'
            ]
        },
        {
            'job_title': 'Software Engineering Intern',
            'company': 'Cloud Solutions Inc',
            'location': 'Remote',
            'start_date': 'May 2019',
            'end_date': 'Aug 2019',
            'responsibilities': [
                'Assisted in developing cloud-based microservices using AWS Lambda',
                'Wrote unit and integration tests achieving 85% code coverage',
                'Documented API endpoints and created user guides'
            ]
        }
    ]
    
    creator.cv_data['skills'] = [
        'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js', 
        'Flask', 'FastAPI', 'SQL', 'MongoDB', 'Docker', 'Kubernetes',
        'AWS', 'Git', 'CI/CD', 'Agile/Scrum'
    ]
    
    creator.cv_data['languages'] = [
        {'name': 'English', 'proficiency': 'Native'},
        {'name': 'French', 'proficiency': 'Intermediate'}
    ]
    
    creator.cv_data['certifications'] = [
        {
            'name': 'AWS Certified Developer - Associate',
            'issuer': 'Amazon Web Services',
            'date': 'January 2022',
            'credential_id': 'AWS-DEV-78901'
        },
        {
            'name': 'Professional Scrum Master I',
            'issuer': 'Scrum.org',
            'date': 'March 2021',
            'credential_id': 'PSM1-45678'
        }
    ]
    
    # Generate and display CV
    print("\n" + "=" * 70)
    print("  GENERATED CV PREVIEW")
    print("=" * 70)
    cv_text = creator.generate_cv_text()
    print(cv_text)
    
    # Save the demo CV
    print("\n" + "=" * 70)
    print("  SAVING DEMO CV")
    print("=" * 70)
    json_file, txt_file = creator.save_cv("demo_cv")
    
    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    print(f"\nDemo CV files created:")
    print(f"  • {json_file}")
    print(f"  • {txt_file}")
    print("\nYou can now:")
    print("  1. View the generated files")
    print("  2. Run the interactive app: python3 cv_creator.py")
    print("  3. Edit the JSON file and re-import it")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    try:
        demo_cv_creator()
    except Exception as e:
        print(f"\n✗ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
