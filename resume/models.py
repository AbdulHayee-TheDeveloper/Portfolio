"""
Django Models for Portfolio Website
All models are fully manageable through Django admin panel
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


# ======================== EXPERIENCE MODEL (Enhanced with Skills) ========================

class Experience(models.Model):
    """
    Work experience, professional history, and skills
    Handles both job experiences and technical skills
    """
    EXPERIENCE_TYPE_CHOICES = [
        ('job', 'Job Experience'),
        ('skill', 'Technical Skill'),
    ]
    
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]
    
    # Type selector
    experience_type = models.CharField(
        max_length=20,
        choices=EXPERIENCE_TYPE_CHOICES,
        default='job',
        verbose_name="Type",
        help_text="Job Experience ya Technical Skill?"
    )
    
    # Common fields
    title = models.CharField(
        max_length=200, 
        verbose_name="Title",
        help_text="Job Title (e.g., Full Stack Developer) OR Skill Name (e.g., Python)",
        default="Title"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Job description OR Skill description"
    )
    
    # Job-specific fields
    company = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="Company Name",
        help_text="Only for Job Experience",
        default="Company Name"
    )
    location = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="Location",
        help_text="Only for Job Experience"
    )
    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Start Date",
        help_text="Only for Job Experience"
    )
    end_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="End Date",
        help_text="Only for Job Experience"
    )
    ongoing = models.BooleanField(
        default=False, 
        verbose_name="Currently Working Here",
        help_text="Only for Job Experience"
    )
    
    # Skill-specific fields
    proficiency = models.CharField(
        max_length=50, 
        choices=PROFICIENCY_CHOICES, 
        blank=True,
        verbose_name="Proficiency Level",
        help_text="Only for Technical Skills"
    )
    category = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Category",
        help_text="e.g., Programming, Framework, Database (for Skills)"
    )
    
    # Media
    icon = models.ImageField(
        upload_to='experience/', 
        blank=True, 
        null=True,
        verbose_name="Logo/Icon",
        help_text="Company logo OR Skill icon"
    )
    
    # Display settings
    visible = models.BooleanField(default=True, verbose_name="Show on Website")
    order = models.IntegerField(
        default=0, 
        verbose_name="Display Order",
        help_text="Lower numbers appear first"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'Experience / Skill'
        verbose_name_plural = 'Experiences / Skills'
    
    def __str__(self):
        if self.experience_type == 'skill':
            return f"[SKILL] {self.title} ({self.proficiency})"
        return f"[JOB] {self.title} at {self.company}"
    
    def is_job(self):
        """Check if this is a job experience"""
        return self.experience_type == 'job'
    
    def is_skill(self):
        """Check if this is a technical skill"""
        return self.experience_type == 'skill'


# ======================== EDUCATION MODEL ========================

class Education(models.Model):
    """
    Educational background and certifications
    """
    DEGREE_LEVELS = [
        ("hs", "Primary & Secondary "),
        ("hs", "Higher Secondary "),
        ("ug", "Undergraduate"),
        ("pg", "Postgraduate"),
        ("cert", "Certification"),
        ("other", "Other"),
    ]

    title = models.CharField(
        max_length=200, 
        verbose_name="Degree/Certificate Title",
        help_text="e.g., BSc Computer Science",
        default="Degree/Certificate Title"
    )
    institution = models.CharField(max_length=200, verbose_name="Institution Name")
    location = models.CharField(max_length=140, blank=True, verbose_name="Location")
    degree_level = models.CharField(
        max_length=12, 
        choices=DEGREE_LEVELS, 
        default="other",
        verbose_name="Degree Level"
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    ongoing = models.BooleanField(
        default=False, 
        verbose_name="Currently Studying",
        help_text="Check if still studying"
    )
    grade_or_gpa = models.CharField(
        max_length=80, 
        blank=True, 
        verbose_name="Grade/GPA"
    )
    summary = models.TextField(
        blank=True, 
        verbose_name="Summary",
        help_text="Short description, projects, honors, or relevant coursework"
    )
    logo = models.ImageField(
        upload_to="education/logos/", 
        null=True, 
        blank=True,
        verbose_name="Institution Logo"
    )
    
    # Display settings
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Display Order",
        help_text="Lower numbers appear first"
    )
    visible = models.BooleanField(default=True, verbose_name="Show on Website")
    
    # Metadata
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.title} — {self.institution}"


# ======================== PROJECT MODEL ========================

class Project(models.Model):
    """
    Portfolio projects showcase
    """
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Upcoming', 'Upcoming'),
    ]
    
    title = models.CharField(
        max_length=200, 
        verbose_name="Project Title",
        help_text='Project title',
        default="Project Title"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Description",
        help_text='Project description'
    )
    path = models.CharField(
        max_length=500, 
        verbose_name="Image Path",
        help_text='Static image path (e.g., images/project1.jpg)',
        blank=True
    )
    demo = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Demo URL",
        help_text='Live demo link (optional)'
    )
    github = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="GitHub URL",
        help_text="GitHub repository link (optional)"
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Project Status"
    )
    tech_stack = models.CharField(
        max_length=500, 
        blank=True,
        verbose_name="Technologies",
        help_text='Comma-separated (e.g., Django, Python, Bootstrap)'
    )
    
    # Display settings
    is_featured = models.BooleanField(
        default=False, 
        verbose_name="Featured Project",
        help_text='Homepage par show karna hai?'
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="Display Order",
        help_text='Lower number appears first'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return self.title
    
    @property
    def tech(self):
        """Convert tech_stack string to list"""
        if self.tech_stack:
            return [tech.strip() for tech in self.tech_stack.split(',')]
        return []
    
    def get_absolute_url(self):
        """Get project detail URL"""
        return reverse('project_detail', args=[str(self.id)])


# ======================== SERVICE MODEL ========================

class Service(models.Model):
    """
    Services offered to clients
    """
    title = models.CharField(max_length=160, verbose_name="Service Title")
    short_description = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name="Short Description",
        default="Short Description"
    )
    description = models.TextField(blank=True, verbose_name="Full Description")
    details = models.TextField(
        blank=True, 
        verbose_name="Service Details",
        help_text='Each point on a new line'
    )
    icon = models.CharField(
        max_length=80, 
        blank=True,
        verbose_name="Icon Class",
        help_text='Font Awesome class (e.g., fa-code) or emoji'
    )
    image = models.ImageField(
        upload_to='services/', 
        blank=True, 
        null=True,
        verbose_name="Service Image"
    )
    link = models.URLField(blank=True, verbose_name="Service Link")
    category = models.CharField(
        max_length=80, 
        blank=True,
        verbose_name="Category"
    )
    duration = models.CharField(
        max_length=80, 
        blank=True,
        verbose_name="Duration",
        help_text="e.g., 2-4 weeks"
    )
    
    # Display settings
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    visible = models.BooleanField(default=True, verbose_name="Show on Website")
    
    # Metadata
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Get service detail URL"""
        return reverse('service_detail', args=[str(self.pk)])


# ======================== CONTACT MODEL ========================

class Contact(models.Model):
    """
    Contact form submissions from visitors
    """
    name = models.CharField(max_length=200, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Phone Number"
    )
    message = models.TextField(verbose_name="Message")
    
    # Status tracking
    is_read = models.BooleanField(default=False, verbose_name="Mark as Read")
    replied = models.BooleanField(default=False, verbose_name="Replied")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    def get_short_message(self):
        """Returns first 50 characters of message"""
        return self.message[:50] + '...' if len(self.message) > 50 else self.message
