
def get_team_identifier(group, request):
    """Rate limit by team ID instead of IP"""
    if request.user.is_authenticated:
        return f"team_{request.user.id}"
    return request.META.get('REMOTE_ADDR')