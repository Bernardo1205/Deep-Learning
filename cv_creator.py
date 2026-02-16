#!/usr/bin/env python3
"""
CV Creator Application
A simple command-line application to help users create their own CV (Curriculum Vitae)
"""

import json
import os
from datetime import datetime


class CVCreator:
    """Class to handle CV creation and management"""
    
    def __init__(self):
        self.cv_data = {
            'personal_info': {},
            'education': [],
            'experience': [],
            'skills': [],
            'languages': [],
            'certifications': []
        }
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self, text):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60 + "\n")
    
    def get_personal_info(self):
        """Collect personal information from the user"""
        self.print_header("Personal Information")
        
        self.cv_data['personal_info']['full_name'] = input("Full Name: ").strip()
        self.cv_data['personal_info']['email'] = input("Email: ").strip()
        self.cv_data['personal_info']['phone'] = input("Phone: ").strip()
        self.cv_data['personal_info']['location'] = input("Location (City, Country): ").strip()
        self.cv_data['personal_info']['linkedin'] = input("LinkedIn Profile (optional): ").strip()
        self.cv_data['personal_info']['github'] = input("GitHub Profile (optional): ").strip()
        self.cv_data['personal_info']['summary'] = input("Professional Summary (brief description): ").strip()
    
    def get_education(self):
        """Collect education information"""
        self.print_header("Education")
        
        while True:
            print("\nAdd Education Entry")
            print("-" * 40)
            
            education = {}
            education['degree'] = input("Degree (e.g., Bachelor of Science): ").strip()
            education['field'] = input("Field of Study: ").strip()
            education['institution'] = input("Institution/University: ").strip()
            education['location'] = input("Location: ").strip()
            education['start_date'] = input("Start Date (e.g., Sept 2018): ").strip()
            education['end_date'] = input("End Date (or 'Present'): ").strip()
            education['gpa'] = input("GPA (optional): ").strip()
            education['achievements'] = input("Key Achievements (optional): ").strip()
            
            self.cv_data['education'].append(education)
            
            more = input("\nAdd another education entry? (y/n): ").strip().lower()
            if more != 'y':
                break
    
    def get_experience(self):
        """Collect work experience information"""
        self.print_header("Work Experience")
        
        while True:
            print("\nAdd Work Experience Entry")
            print("-" * 40)
            
            experience = {}
            experience['job_title'] = input("Job Title: ").strip()
            experience['company'] = input("Company Name: ").strip()
            experience['location'] = input("Location: ").strip()
            experience['start_date'] = input("Start Date (e.g., Jan 2020): ").strip()
            experience['end_date'] = input("End Date (or 'Present'): ").strip()
            
            print("\nJob Responsibilities (enter one per line, empty line to finish):")
            responsibilities = []
            while True:
                resp = input("- ").strip()
                if not resp:
                    break
                responsibilities.append(resp)
            experience['responsibilities'] = responsibilities
            
            self.cv_data['experience'].append(experience)
            
            more = input("\nAdd another work experience? (y/n): ").strip().lower()
            if more != 'y':
                break
    
    def get_skills(self):
        """Collect skills information"""
        self.print_header("Skills")
        
        print("Enter your skills (comma-separated):")
        print("Example: Python, Machine Learning, Data Analysis, TensorFlow")
        skills_input = input("Skills: ").strip()
        
        if skills_input:
            self.cv_data['skills'] = [skill.strip() for skill in skills_input.split(',')]
    
    def get_languages(self):
        """Collect language proficiency information"""
        self.print_header("Languages")
        
        while True:
            print("\nAdd Language")
            print("-" * 40)
            
            language = {}
            language['name'] = input("Language: ").strip()
            language['proficiency'] = input("Proficiency (e.g., Native, Fluent, Intermediate): ").strip()
            
            self.cv_data['languages'].append(language)
            
            more = input("\nAdd another language? (y/n): ").strip().lower()
            if more != 'y':
                break
    
    def get_certifications(self):
        """Collect certification information"""
        self.print_header("Certifications")
        
        while True:
            print("\nAdd Certification")
            print("-" * 40)
            
            cert = {}
            cert['name'] = input("Certification Name: ").strip()
            cert['issuer'] = input("Issuing Organization: ").strip()
            cert['date'] = input("Date Obtained: ").strip()
            cert['credential_id'] = input("Credential ID (optional): ").strip()
            
            self.cv_data['certifications'].append(cert)
            
            more = input("\nAdd another certification? (y/n): ").strip().lower()
            if more != 'y':
                break
    
    def generate_cv_text(self):
        """Generate a formatted text version of the CV"""
        cv_text = []
        
        # Personal Information
        pi = self.cv_data['personal_info']
        cv_text.append("=" * 80)
        cv_text.append(f"{pi.get('full_name', 'N/A').upper()}")
        cv_text.append("=" * 80)
        cv_text.append(f"Email: {pi.get('email', 'N/A')} | Phone: {pi.get('phone', 'N/A')}")
        cv_text.append(f"Location: {pi.get('location', 'N/A')}")
        
        if pi.get('linkedin'):
            cv_text.append(f"LinkedIn: {pi['linkedin']}")
        if pi.get('github'):
            cv_text.append(f"GitHub: {pi['github']}")
        
        cv_text.append("\n" + "-" * 80)
        cv_text.append("PROFESSIONAL SUMMARY")
        cv_text.append("-" * 80)
        cv_text.append(pi.get('summary', 'N/A'))
        
        # Education
        if self.cv_data['education']:
            cv_text.append("\n" + "-" * 80)
            cv_text.append("EDUCATION")
            cv_text.append("-" * 80)
            for edu in self.cv_data['education']:
                cv_text.append(f"\n{edu.get('degree', 'N/A')} in {edu.get('field', 'N/A')}")
                cv_text.append(f"{edu.get('institution', 'N/A')}, {edu.get('location', 'N/A')}")
                cv_text.append(f"{edu.get('start_date', 'N/A')} - {edu.get('end_date', 'N/A')}")
                if edu.get('gpa'):
                    cv_text.append(f"GPA: {edu['gpa']}")
                if edu.get('achievements'):
                    cv_text.append(f"Achievements: {edu['achievements']}")
        
        # Work Experience
        if self.cv_data['experience']:
            cv_text.append("\n" + "-" * 80)
            cv_text.append("WORK EXPERIENCE")
            cv_text.append("-" * 80)
            for exp in self.cv_data['experience']:
                cv_text.append(f"\n{exp.get('job_title', 'N/A')}")
                cv_text.append(f"{exp.get('company', 'N/A')}, {exp.get('location', 'N/A')}")
                cv_text.append(f"{exp.get('start_date', 'N/A')} - {exp.get('end_date', 'N/A')}")
                if exp.get('responsibilities'):
                    cv_text.append("Responsibilities:")
                    for resp in exp['responsibilities']:
                        cv_text.append(f"  • {resp}")
        
        # Skills
        if self.cv_data['skills']:
            cv_text.append("\n" + "-" * 80)
            cv_text.append("SKILLS")
            cv_text.append("-" * 80)
            cv_text.append(", ".join(self.cv_data['skills']))
        
        # Languages
        if self.cv_data['languages']:
            cv_text.append("\n" + "-" * 80)
            cv_text.append("LANGUAGES")
            cv_text.append("-" * 80)
            for lang in self.cv_data['languages']:
                cv_text.append(f"  • {lang.get('name', 'N/A')}: {lang.get('proficiency', 'N/A')}")
        
        # Certifications
        if self.cv_data['certifications']:
            cv_text.append("\n" + "-" * 80)
            cv_text.append("CERTIFICATIONS")
            cv_text.append("-" * 80)
            for cert in self.cv_data['certifications']:
                cv_text.append(f"  • {cert.get('name', 'N/A')}")
                cv_text.append(f"    {cert.get('issuer', 'N/A')}, {cert.get('date', 'N/A')}")
                if cert.get('credential_id'):
                    cv_text.append(f"    Credential ID: {cert['credential_id']}")
        
        cv_text.append("\n" + "=" * 80)
        
        return "\n".join(cv_text)
    
    def save_cv(self, filename_prefix="my_cv"):
        """Save CV in both JSON and text formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_filename = f"{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.cv_data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ CV data saved as: {json_filename}")
        
        # Save as text
        txt_filename = f"{filename_prefix}_{timestamp}.txt"
        cv_text = self.generate_cv_text()
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(cv_text)
        print(f"✓ CV document saved as: {txt_filename}")
        
        return json_filename, txt_filename
    
    def preview_cv(self):
        """Display a preview of the CV"""
        self.clear_screen()
        self.print_header("CV PREVIEW")
        print(self.generate_cv_text())
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        self.clear_screen()
        print("\n" + "=" * 60)
        print("  Welcome to CV Creator!")
        print("  Create Your Professional CV Step by Step")
        print("=" * 60)
        input("\nPress Enter to begin...")
        
        # Collect all information
        self.get_personal_info()
        self.get_education()
        self.get_experience()
        self.get_skills()
        
        # Optional sections
        add_languages = input("\nWould you like to add languages? (y/n): ").strip().lower()
        if add_languages == 'y':
            self.get_languages()
        
        add_certs = input("\nWould you like to add certifications? (y/n): ").strip().lower()
        if add_certs == 'y':
            self.get_certifications()
        
        # Preview and save
        self.preview_cv()
        
        self.print_header("Save Your CV")
        filename_prefix = input("Enter filename prefix (default: my_cv): ").strip() or "my_cv"
        
        json_file, txt_file = self.save_cv(filename_prefix)
        
        print("\n" + "=" * 60)
        print("  CV Creation Complete!")
        print("=" * 60)
        print(f"\nYour CV has been saved in two formats:")
        print(f"  1. JSON format: {json_file} (for easy editing)")
        print(f"  2. Text format: {txt_file} (ready to use)")
        print("\nThank you for using CV Creator!")
        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    try:
        creator = CVCreator()
        creator.run()
    except KeyboardInterrupt:
        print("\n\nCV creation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try again.")


if __name__ == "__main__":
    main()
