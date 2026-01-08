# blog/context_processors.py
import requests
from datetime import datetime
import pytz
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def world_time(request):
    """Add world times to template context"""
    context = {
        'ireland_time': None,
        'ethiopia_time': None,
        'time_error': False,
    }
    
    try:
        # Get Ireland time
        ireland_response = requests.get(
            "https://worldtimeapi.org/api/timezone/Europe/Dublin",
            timeout=3  # 3 second timeout
        )
        ireland_response.raise_for_status()
        ireland_data = ireland_response.json()
        ireland_dt = datetime.fromisoformat(ireland_data['datetime'].replace('Z', '+00:00'))
        context['ireland_time'] = ireland_dt.strftime('%I:%M %p')  # 12-hour format
        context['ireland_date'] = ireland_dt.strftime('%b %d, %Y')
        context['ireland_timezone'] = 'Europe/Dublin'
        
    except requests.exceptions.RequestException as e:
        logger.warning(f"Could not fetch Ireland time: {e}")
        context['time_error'] = True
        # Fallback to local server time for Ireland
        ireland_tz = pytz.timezone('Europe/Dublin')
        ireland_dt = datetime.now(ireland_tz)
        context['ireland_time'] = ireland_dt.strftime('%I:%M %p')
        context['ireland_date'] = ireland_dt.strftime('%b %d, %Y')
        context['ireland_timezone'] = 'Europe/Dublin (estimated)'
    
    try:
        # Get Ethiopia time
        ethiopia_response = requests.get(
            "https://worldtimeapi.org/api/timezone/Africa/Addis_Ababa",
            timeout=3
        )
        ethiopia_response.raise_for_status()
        ethiopia_data = ethiopia_response.json()
        ethiopia_dt = datetime.fromisoformat(ethiopia_data['datetime'].replace('Z', '+00:00'))
        context['ethiopia_time'] = ethiopia_dt.strftime('%I:%M %p')
        context['ethiopia_date'] = ethiopia_dt.strftime('%b %d, %Y')
        context['ethiopia_timezone'] = 'Africa/Addis_Ababa'
        
    except requests.exceptions.RequestException as e:
        logger.warning(f"Could not fetch Ethiopia time: {e}")
        context['time_error'] = True
        # Fallback to local server time for Ethiopia
        ethiopia_tz = pytz.timezone('Africa/Addis_Ababa')
        ethiopia_dt = datetime.now(ethiopia_tz)
        context['ethiopia_time'] = ethiopia_dt.strftime('%I:%M %p')
        context['ethiopia_date'] = ethiopia_dt.strftime('%b %d, %Y')
        context['ethiopia_timezone'] = 'Africa/Addis_Ababa (estimated)'
    
    # Calculate time difference
    if context['ireland_time'] and context['ethiopia_time']:
        try:
            # Create datetime objects for comparison
            ireland_tz = pytz.timezone('Europe/Dublin')
            ethiopia_tz = pytz.timezone('Africa/Addis_Ababa')
            
            ireland_now = datetime.now(ireland_tz)
            ethiopia_now = datetime.now(ethiopia_tz)
            
            # Calculate hour difference
            diff = ethiopia_now - ireland_now
            hours_diff = diff.total_seconds() / 3600
            
            if -1 < hours_diff < 1:
                context['time_difference'] = "Same time"
            elif hours_diff > 0:
                context['time_difference'] = f"Ethiopia is {int(hours_diff)} hours ahead"
            else:
                context['time_difference'] = f"Ethiopia is {int(abs(hours_diff))} hours behind"
                
        except:
            context['time_difference'] = "Different time zones"
    
    return context