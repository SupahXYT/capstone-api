# Nothing like brute forcing solutions 
# Who needs nlp?
CATEGORIES = {

    'identifier': [
    r'(user)?name',
    r'(postal|home) address', 
    r'(postal|zip) code',
    'account information',
    'alias'],

    'device': [
    r'device (idenfier|information)',
    'psuedonym',
    'email', 
    'phone', 
    'ip address', 
    'internet protocol', 
    'mobile advertising id', 
    'maid', 
    'idfa', 
    'aaid', 
    'cookie'],

    'government_record': [
    r'passport|ssn|(social security)', 
    r'(state|government) id'],

    'protected_characteristic': [
    r'race|ethnicity', 
    r'religion|religious', 
    r'marital|marriage', 
    r'gender|sex', 
    'political', 
    'spoken language',
    'characteristic',
    'demographic'],

    'internet_activity': [
    r'(internet|network) activity', 
    r'(browsing|search) history'],

    # should I even include this?
    'commercial': [
    'commercial information',
    'property records',
    'personal property',
    'business data',
    'purchase'],

    'geolocation': [
    r'geo ?location',
    r'(percise )?location',
    'gps',
    'global positioning',
    'geographic'],

    'biometric': [r'biometric|health'],

    'employment': [r'professional|employ(ment|er|ee)'],

    'education': [r'education(al)?'],

    'inference': [r'derive|inference']

}

