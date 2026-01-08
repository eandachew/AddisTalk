# blog/context_processors.py
import requests
from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)

def world_time(request):
    """Add world times to template context"""
    context = {
        'ireland_time': None,
        'ethiopia_time': None,
        'time_error': False,
    }
    
    # Increase timeout to 10 seconds
    timeout = 10
    
    try:
        # Get Ireland time
        ireland_response = requests.get(
            "https://worldtimeapi.org/api/timezone/Europe/Dublin",
            timeout=timeout
        )
        ireland_response.raise_for_status()
        ireland_data = ireland_response.json()
        
        ireland_dt_str = ireland_data['datetime']
        if 'Z' in ireland_dt_str:
            ireland_dt = datetime.fromisoformat(ireland_dt_str.replace('Z', '+00:00'))
        else:
            ireland_dt = datetime.fromisoformat(ireland_dt_str)
        
        context['ireland_time'] = ireland_dt.strftime('%I:%M %p')
        context['ireland_date'] = ireland_dt.strftime('%b %d, %Y')
        context['ireland_timezone'] = 'Europe/Dublin'
        
    except Exception as e:
        logger.error(f"Ireland time error: {e}")
        context['time_error'] = True
        # Fallback
        now_utc = datetime.now(timezone.utc)
        context['ireland_time'] = now_utc.strftime('%I:%M %p')
        context['ireland_date'] = now_utc.strftime('%b %d, %Y')
        context['ireland_timezone'] = 'Europe/Dublin (est.)'
    
    try:
        # Get Ethiopia time
        ethiopia_response = requests.get(
            "https://worldtimeapi.org/api/timezone/Africa/Addis_Ababa",
            timeout=timeout
        )
        ethiopia_response.raise_for_status()
        ethiopia_data = ethiopia_response.json()
        
        ethiopia_dt_str = ethiopia_data['datetime']
        if 'Z' in ethiopia_dt_str:
            ethiopia_dt = datetime.fromisoformat(ethiopia_dt_str.replace('Z', '+00:00'))
        else:
            ethiopia_dt = datetime.fromisoformat(ethiopia_dt_str)
        
        context['ethiopia_time'] = ethiopia_dt.strftime('%I:%M %p')
        context['ethiopia_date'] = ethiopia_dt.strftime('%b %d, %Y')
        context['ethiopia_timezone'] = 'Africa/Addis_Ababa'
        
    except Exception as e:
        logger.error(f"Ethiopia time error: {e}")
        context['time_error'] = True
        # Fallback (Ethiopia is UTC+3)
        now_utc = datetime.now(timezone.utc)
        ethiopia_dt = now_utc + timedelta(hours=3)
        context['ethiopia_time'] = ethiopia_dt.strftime('%I:%M %p')
        context['ethiopia_date'] = ethiopia_dt.strftime('%b %d, %Y')
        context['ethiopia_timezone'] = 'Africa/Addis_Ababa (est.)'
    
    # Only show "estimated" message if BOTH failed
    if context['ireland_timezone'].endswith('(est.)') and context['ethiopia_timezone'].endswith('(est.)'):
        context['time_error'] = True
    else:
        context['time_error'] = False
    
    # Calculate difference
    if 'time_difference' not in context:
        context['time_difference'] = "Ethiopia is 3 hours ahead"
    
    return context