#!/usr/bin/env python3
"""
Test script for CV Creator Application
This script tests the CV creator with sample data
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cv_creator import CVCreator


def test_cv_creator():
    """Test the CV creator with sample data"""
    print("Testing CV Creator Application...")
    print("=" * 60)
    
    # Create instance
    creator = CVCreator()
    
    # Test 1: Add personal information
    print("\nTest 1: Adding personal information...")
    creator.cv_data['personal_info'] = {
        'full_name': 'Jane Smith',
        'email': 'jane.smith@email.com',
        'phone': '+1-555-123-4567',
        'location': 'San Francisco, CA',
        'linkedin': 'linkedin.com/in/janesmith',
        'github': 'github.com/janesmith',
        'summary': 'Experienced data scientist with expertise in machine learning and deep learning.'
    }
    print("✓ Personal information added")
    
    # Test 2: Add education
    print("\nTest 2: Adding education...")
    creator.cv_data['education'] = [
        {
            'degree': 'Master of Science',
            'field': 'Computer Science',
            'institution': 'Stanford University',
            'location': 'Stanford, CA',
            'start_date': 'Sept 2018',
            'end_date': 'June 2020',
            'gpa': '3.9/4.0',
            'achievements': 'Dean\'s List, Research Assistant'
        },
        {
            'degree': 'Bachelor of Science',
            'field': 'Mathematics',
            'institution': 'UC Berkeley',
            'location': 'Berkeley, CA',
            'start_date': 'Sept 2014',
            'end_date': 'May 2018',
            'gpa': '3.8/4.0',
            'achievements': 'Summa Cum Laude'
        }
    ]
    print("✓ Education entries added")
    
    # Test 3: Add work experience
    print("\nTest 3: Adding work experience...")
    creator.cv_data['experience'] = [
        {
            'job_title': 'Senior Data Scientist',
            'company': 'Tech Corp',
            'location': 'San Francisco, CA',
            'start_date': 'Jan 2021',
            'end_date': 'Present',
            'responsibilities': [
                'Led ML model development for recommendation systems',
                'Improved model accuracy by 25%',
                'Mentored team of 3 junior data scientists'
            ]
        },
        {
            'job_title': 'Data Scientist',
            'company': 'StartUp Inc',
            'location': 'Palo Alto, CA',
            'start_date': 'July 2020',
            'end_date': 'Dec 2020',
            'responsibilities': [
                'Developed predictive models using Python and TensorFlow',
                'Created data pipelines for ETL processes',
                'Collaborated with cross-functional teams'
            ]
        }
    ]
    print("✓ Work experience added")
    
    # Test 4: Add skills
    print("\nTest 4: Adding skills...")
    creator.cv_data['skills'] = [
        'Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 
        'PyTorch', 'SQL', 'Data Analysis', 'Statistical Modeling'
    ]
    print("✓ Skills added")
    
    # Test 5: Add languages
    print("\nTest 5: Adding languages...")
    creator.cv_data['languages'] = [
        {'name': 'English', 'proficiency': 'Native'},
        {'name': 'Spanish', 'proficiency': 'Fluent'}
    ]
    print("✓ Languages added")
    
    # Test 6: Add certifications
    print("\nTest 6: Adding certifications...")
    creator.cv_data['certifications'] = [
        {
            'name': 'AWS Certified Machine Learning - Specialty',
            'issuer': 'Amazon Web Services',
            'date': 'March 2021',
            'credential_id': 'AWS-ML-12345'
        }
    ]
    print("✓ Certifications added")
    
    # Test 7: Generate CV text
    print("\nTest 7: Generating CV text...")
    cv_text = creator.generate_cv_text()
    assert len(cv_text) > 0, "CV text should not be empty"
    assert 'JANE SMITH' in cv_text, "CV should contain full name"
    assert 'jane.smith@email.com' in cv_text, "CV should contain email"
    assert 'Stanford University' in cv_text, "CV should contain education"
    assert 'Tech Corp' in cv_text, "CV should contain work experience"
    print("✓ CV text generated successfully")
    
    # Test 8: Save CV files
    print("\nTest 8: Saving CV files...")
    json_file, txt_file = creator.save_cv("test_cv")
    
    # Verify files exist
    assert os.path.exists(json_file), f"JSON file {json_file} should exist"
    assert os.path.exists(txt_file), f"Text file {txt_file} should exist"
    print(f"✓ CV saved as {json_file} and {txt_file}")
    
    # Test 9: Verify file contents
    print("\nTest 9: Verifying file contents...")
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'JANE SMITH' in content, "Text file should contain name"
        assert 'EDUCATION' in content, "Text file should contain education section"
        assert 'WORK EXPERIENCE' in content, "Text file should contain experience section"
    print("✓ File contents verified")
    
    # Display preview
    print("\n" + "=" * 60)
    print("CV Preview:")
    print("=" * 60)
    print(cv_text)
    
    # Cleanup test files
    print("\n" + "=" * 60)
    print("Cleaning up test files...")
    if os.path.exists(json_file):
        os.remove(json_file)
        print(f"✓ Removed {json_file}")
    if os.path.exists(txt_file):
        os.remove(txt_file)
        print(f"✓ Removed {txt_file}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_cv_creator()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
