from .models import Accomplishment, Education, Experience, Interest, User


def save_scraped_user_data(scraped_data):
    """
    Save scraped LinkedIn data to database models

    Args:
        scraped_data (dict): The scraped data in the format returned by the scraper

    Returns:
        User: The created or updated User instance
    """
    linkedin_url = scraped_data.get("linkedin_url")
    if not linkedin_url:
        raise ValueError("LinkedIn URL is required")

    # Create or update user
    user, created = User.objects.get_or_create(
        linkedin_url=linkedin_url,
        defaults={
            "name": scraped_data.get("name"),
            "job_title": scraped_data.get("job_title"),
            "company": scraped_data.get("company"),
            "location": scraped_data.get("location"),
            "about": scraped_data.get("about"),
        },
    )

    # If user already exists, update the basic info
    if not created:
        user.name = scraped_data.get("name") or user.name
        user.job_title = scraped_data.get("job_title") or user.job_title
        user.company = scraped_data.get("company") or user.company
        user.location = scraped_data.get("location") or user.location
        user.about = scraped_data.get("about") or user.about
        user.save()

    # Clear existing related data to replace with new data
    if not created:
        user.experiences.all().delete()
        user.educations.all().delete()
        user.interests.all().delete()
        user.accomplishments.all().delete()

    # Save experiences
    experiences_data = scraped_data.get("experiences", [])
    for exp_data in experiences_data:
        Experience.objects.create(
            user=user,
            institution_name=exp_data.get("institution_name"),
            linkedin_url=exp_data.get("linkedin_url"),
            website=exp_data.get("website"),
            industry=exp_data.get("industry"),
            type=exp_data.get("type"),
            headquarters=exp_data.get("headquarters"),
            company_size=exp_data.get("company_size"),
            founded=exp_data.get("founded"),
            position_title=exp_data.get("position_title"),
            from_date=exp_data.get("from_date"),
            to_date=exp_data.get("to_date"),
            duration=exp_data.get("duration"),
            location=exp_data.get("location"),
            description=exp_data.get("description"),
        )

    # Save educations
    educations_data = scraped_data.get("educations", [])
    for edu_data in educations_data:
        Education.objects.create(
            user=user,
            institution_name=edu_data.get("institution_name"),
            linkedin_url=edu_data.get("linkedin_url"),
            website=edu_data.get("website"),
            industry=edu_data.get("industry"),
            type=edu_data.get("type"),
            headquarters=edu_data.get("headquarters"),
            company_size=edu_data.get("company_size"),
            founded=edu_data.get("founded"),
            degree=edu_data.get("degree"),
            from_date=edu_data.get("from_date"),
            to_date=edu_data.get("to_date"),
            description=edu_data.get("description"),
        )

    # Save interests
    interests_data = scraped_data.get("interests", [])
    for interest_data in interests_data:
        if isinstance(interest_data, dict):
            name = interest_data.get("name", "")
        else:
            name = str(interest_data)

        if name:
            Interest.objects.create(user=user, name=name)

    # Save accomplishments
    accomplishments_data = scraped_data.get("accomplishments", [])
    for acc_data in accomplishments_data:
        if isinstance(acc_data, dict):
            title = acc_data.get("title", "")
            description = acc_data.get("description", "")
        else:
            title = str(acc_data)
            description = ""

        if title:
            Accomplishment.objects.create(
                user=user, title=title, description=description
            )

    return user


def get_user_data_by_linkedin_url(linkedin_url):
    """
    Retrieve user data from database by LinkedIn URL

    Args:
        linkedin_url (str): The LinkedIn profile URL

    Returns:
        dict: User data in the same format as scraper output, or None if not found
    """
    try:
        user = User.objects.get(linkedin_url=linkedin_url)
    except User.DoesNotExist:
        return None

    # Convert database data back to scraper format
    user_data = {
        "name": user.name,
        "job_title": user.job_title,
        "company": user.company,
        "location": user.location,
        "about": user.about,
        "linkedin_url": user.linkedin_url,
        "experiences": [],
        "educations": [],
        "interests": [],
        "accomplishments": [],
    }

    # Add experiences
    for exp in user.experiences.all():
        user_data["experiences"].append(
            {
                "institution_name": exp.institution_name,
                "linkedin_url": exp.linkedin_url,
                "website": exp.website,
                "industry": exp.industry,
                "type": exp.type,
                "headquarters": exp.headquarters,
                "company_size": exp.company_size,
                "founded": exp.founded,
                "position_title": exp.position_title,
                "from_date": exp.from_date,
                "to_date": exp.to_date,
                "duration": exp.duration,
                "location": exp.location,
                "description": exp.description,
            }
        )

    # Add educations
    for edu in user.educations.all():
        user_data["educations"].append(
            {
                "institution_name": edu.institution_name,
                "linkedin_url": edu.linkedin_url,
                "website": edu.website,
                "industry": edu.industry,
                "type": edu.type,
                "headquarters": edu.headquarters,
                "company_size": edu.company_size,
                "founded": edu.founded,
                "degree": edu.degree,
                "from_date": edu.from_date,
                "to_date": edu.to_date,
                "description": edu.description,
            }
        )

    # Add interests
    for interest in user.interests.all():
        user_data["interests"].append(interest.name)

    # Add accomplishments
    for acc in user.accomplishments.all():
        user_data["accomplishments"].append(acc.title)

    return user_data


def user_exists_in_db(linkedin_url):
    """
    Check if a user with the given LinkedIn URL already exists in the database

    Args:
        linkedin_url (str): The LinkedIn profile URL to check

    Returns:
        bool: True if user exists, False otherwise
    """
    return User.objects.filter(linkedin_url=linkedin_url).exists()
