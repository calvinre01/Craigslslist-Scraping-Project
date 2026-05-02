"""
Contains the fuctions and imports needed for sending emails securly
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_emails(port, sender_gmail, receiver_gmail, s_password, results, test):
    """
    Sends and email given the port, sender gmail, reeiver gmail, sender password
    constructs email using results. If there are no results, no email is sent
    If test is true, sends a message to debugging output instead
    """
    if len(results) <= 0:
        print("No results, not sending email")
        return
    # split up results into its different zones
    zones = {
        "zone1": [],
        "zone2": [],
        "zone3": []
    }
    zone_labels = {
        "zone1": "Listings Within 3 hour distance",
        "zone2": "Listings Within 8 hour distance",
        "zone3": "All other Listings"
    }

    for result in results:
        if result["zone"] == 1:
            zones["zone1"].append(result)
        elif result["zone"] == 2:
            zones["zone2"].append(result)
        else:
            zones["zone3"].append(result)
    
    print(f"sending email with {len(results)} results")
    smtp_server = "smtp.gmail.com"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Today's listings"
    msg["From"] = sender_gmail
    msg["To"] = receiver_gmail

    # create both text and html version of the gmail
    text = """\
    Here is a list of todays listings
    """

    html = """\
    <html>
        <body>
            <p>Here is a list of today's listings:</p>
    """
    for zone_name, zone_results in zones.items():
        if not zone_results:
            continue  # skip this zone if it has no listings

        # get zone heading based on zone name
        zone_heading = zone_labels.get(zone_name, "Listings")
        text += f"{zone_heading}\n"
        html += f"<p>{zone_heading}</p>\n<ul>"

        for result in zone_results:
            title = result.get('title', 'No Title')
            price = result.get('price', 'No price')
            url = result.get('url', '#')
            # Append result to plain text version
            text += f"- {title} - {price}\n  {url}\n\n"
            # Append result to HTML version
            html += f'<li><strong>{title}</strong> - {price}<br><a href="{url}">{url}</a></li>\n'

        html += "</ul>\n"

    # close html
    html += """\
        </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    msg.attach(part1)
    msg.attach(part2)

    if test:
    # debug server version
        with smtplib.SMTP("localhost", 1025) as server:
            server.sendmail(sender_gmail, receiver_gmail, msg.as_string())
    else:
        # real gmail version
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_gmail, s_password)
            server.sendmail(sender_gmail, receiver_gmail, msg.as_string())