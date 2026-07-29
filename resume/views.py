"""
Django Views for Portfolio Application
Experience model handles both jobs and skills
"""

import os
from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings

from .models import Experience, Education, Project, Service, Contact
from .forms import ContactForm


# ======================== HOME PAGE ========================

from django.shortcuts import render, redirect

def home(request):
    """
    Main homepage view with integrated contact form
    """
    # Initialize form and success flag
    form = ContactForm()
    success = False
    
    # Handle contact form submission
    if request.method == 'POST':
        print("🔵 POST Request Received")
        form = ContactForm(request.POST)
        
        if form.is_valid():
            print("✅ Form is Valid")
            # Save to database
            contact = form.save()
            print(f"💾 Saved: {contact.id} - {contact.name}")
            
            # Send emails (optional)
            try:
                send_mail(
                    subject=f"New Contact from {contact.name}",
                    message=f"Name: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone or 'Not provided'}\n\nMessage:\n{contact.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['ahayee535@gmail.com'],
                    fail_silently=True,
                )
                
                send_mail(
                    subject="Thanks for contacting Abdul Hayee!",
                    message=f"Hi {contact.name},\n\nThank you for reaching out! I'll get back to you soon.\n\nBest regards,\nAbdul Hayee",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact.email],
                    fail_silently=True,
                )
                print("📧 Emails sent")
            except Exception as e:
                print(f"❌ Email Error: {e}")
            
            # ✅ Redirect to contact section after success
            return redirect('/#contact')  # This scrolls to #contact section
        else:
            print(f"❌ Form Errors: {form.errors}")
    
    # Get all data
    experiences = Experience.objects.filter(experience_type='job', visible=True).order_by('order', '-start_date')
    skills = Experience.objects.filter(experience_type='skill', visible=True).order_by('order', 'title')
    projects_show = Project.objects.all()[:3]
    services = Service.objects.filter(visible=True).order_by('order')
    educations = Education.objects.filter(visible=True).order_by('order', '-start_date')
    total_projects = Project.objects.count()
    
    context = {
        'form': form,
        'success': success,
        'experiences': experiences,
        'skills': skills,
        'projects_show': projects_show,
        'services': services,
        'educations': educations,
        'show_see_more': total_projects > 3,
    }
    
    return render(request, 'base.html', context)




# ======================== EXPERIENCES SECTION ========================

def experiences_view(request):
    """
    Display job experiences only
    """
    experiences = Experience.objects.filter(
        experience_type='job',
        visible=True
    ).order_by('order', '-start_date')
    
    return render(request, 'experiences_section.html', {'experiences': experiences})


# ======================== SKILLS SECTION ========================

def skills_section(request):
    """
    Display technical skills only
    """
    skills = Experience.objects.filter(
        experience_type='skill',
        visible=True
    ).order_by('order', 'title')
    
    return render(request, 'skills_section.html', {'skills': skills})


# ======================== ABOUT SECTION ========================

def about_section(request):
    """
    Render About section with Education items
    """
    educations = Education.objects.filter(visible=True).order_by('order', '-start_date')
    return render(request, 'about_section_fragment.html', {'educations': educations})


# ======================== PROJECTS SECTION ========================

def all_projects(request):
    """
    Display all projects with pagination
    """
    projects_list = Project.objects.all().order_by('-order', '-created_at')
    
    paginator = Paginator(projects_list, 9)
    page_number = request.GET.get('page')
    projects_show = paginator.get_page(page_number)
    
    context = {
        'projects_show': projects_show,
        'show_see_more': False,
    }
    return render(request, 'all_projects.html', context)


def project_detail(request, pk):
    """
    Display individual project details
    """
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})


# ======================== SERVICES SECTION ========================

def services_section(request):
    """
    Display all services
    """
    services = Service.objects.filter(visible=True).order_by('order')
    return render(request, 'service_section.html', {'services': services})


# ======================== CONTACT SECTION ========================

def contact(request):
    """
    Handle contact form submission
    """
    form = ContactForm()
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            try:
                # Send to admin
                send_mail(
                    subject=f"New Contact from {contact.name}",
                    message=f"Name: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone or 'Not provided'}\n\nMessage:\n{contact.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['ahayee535@gmail.com'],
                    fail_silently=False,
                )

                # Send confirmation to user
                send_mail(
                    subject="Thanks for contacting Abdul Hayee!",
                    message=f"Hi {contact.name},\n\nThank you for reaching out! I'll get back to you soon.\n\nBest regards,\nAbdul Hayee",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact.email],
                    fail_silently=False,
                )
                
                success = True
                form = ContactForm()
                
            except Exception as e:
                print(f"Email sending failed: {e}")

    return render(request, 'contact_section.html', {'form': form, 'success': success})


# ======================== RESUME DOWNLOAD ========================

import os
from django.http import FileResponse, Http404, HttpResponse
from django.conf import settings

def resume(request):
    """
    Download resume PDF - Updated for cv.pdf
    """
    # Path to your cv.pdf file
    resume_path = os.path.join(settings.BASE_DIR, 'static', 'myapp', 'resume.pdf')
    
    # Debug: Print path to terminal
    print(f"📄 Looking for resume at: {resume_path}")
    print(f"📁 File exists: {os.path.isfile(resume_path)}")
    
    # Check if file exists
    if not os.path.isfile(resume_path):
        return HttpResponse(
            f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial;
                            padding: 50px;
                            background: #f5f5f5;
                            text-align: center;
                        }}
                        .error-box {{
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                            max-width: 600px;
                            margin: 0 auto;
                        }}
                        h1 {{ color: #dc3545; }}
                        .path {{ 
                            background: #f8f9fa;
                            padding: 10px;
                            border-radius: 5px;
                            word-break: break-all;
                            margin: 20px 0;
                        }}
                        a {{ 
                            color: #007bff;
                            text-decoration: none;
                            font-weight: bold;
                        }}
                    </style>
                </head>
                <body>
                    <div class="error-box">
                        <h1>❌ Resume Not Found</h1>
                        <p><strong>Expected location:</strong></p>
                        <div class="path">{resume_path}</div>
                        <h3>To fix this:</h3>
                        <ol style="text-align: left;">
                            <li>Create folder: <code>static/myapp/</code></li>
                            <li>Add your resume: <code>static/myapp/cv.pdf</code></li>
                            <li>Or rename your file to: <code>resume.pdf</code></li>
                            <li>Refresh this page</li>
                        </ol>
                        <a href="/">← Back to Home</a>
                    </div>
                </body>
            </html>
            """,
            status=404
        )
    
    # File exists, serve it
    try:
        response = FileResponse(
            open(resume_path, 'rb'),
            as_attachment=True,
            filename="Abdul_Hayee_Resume_2025.pdf"  # Downloaded file name
        )
        
        response['Content-Type'] = 'application/pdf'
        response['Content-Length'] = os.path.getsize(resume_path)
        
        print("✅ Resume file served successfully!")
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise Http404(f"Error loading resume: {str(e)}")

