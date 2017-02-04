from api_utils import pull_messages

def show_messages(options, user, partner, inbox):
    pull_messages(inbox, user.id, partner.id,
        loop_limit=options.n, inbox_limit=options.n)
