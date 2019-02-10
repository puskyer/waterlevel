#!/usr/bin/python
# sendemail.pl - Sends email based on a conf file or arguments

# DOCUMENTATION:
#   USAGE:
#     Either:
#       sendemail.py
#       - Checks /mnt/sdcard/tmp/mailout.conf by default
#       sendemail.py <conf file location>
#       - Specify a conf file location
#       sendemail.py <recipient> <subject> <message body>
#       - Specify email details manually
#
#   EXAMPLE CONF FILE LAYOUT:
#     mailto: joe@bloggs.com
#     subject: This is the subject
#     body:
#     This is the body of the message.
#     Note that the actual message begins AFTER the first line break after body:
#     Obviously don't include the # comments on the left, or the indents.
#     Line breaks and spacing should be preserved by most mail clients.
#     Most clients will also handle text wrapping automatically.
#     This will be read all the way until the end of the file.
#
#   QUESTIONS:
#     WHY IS THERE A DEFAULT LOCATION OPTION?:
#     The reason there's a default conf file location with no arguments is
#     because this script was written for use with the Tasker Android app, in
#     conjunction with Android Scripting Environment: at this time, Tasker can't
#     specify arguments when running a script - You will need to use a Tasker
#     File operation to write the file contents before running the script then
#     (preferably) clean up by deleting the file once the script has run.
#
#     WARGH! MY FILE LOCATION IS DIFFERENT AND I WANT TO USE TASKER!:
#     The default location I've entered was tested with my HTC Desire running
#     ASE: You'll need to edit this script, and change the following line:
#       conf_file = '/mnt/sdcard/tmp/mailout.conf'
#     to point to the location of your file. Or wait until Tasker allows you to
#     specify arguments when running a script.
#
#     WHY DO I NEED TO ENTER MY USERNAME/PASSWORD IN PLAINTEXT?:
#     Because there's currently no way authenticate directly with the server and
#     send an Email in the current scripting API - You can only call the mail
#     app with specific arguments and have the Compose window pop up - manual
#     interaction is required to actually send the email - This script bypasses
#     this by interacting and authenticating directly with the Google SMTP
#     server, but in order to do this, your logic details need to be inside the
#     script.
#
#     HOW DO I KNOW YOU AREN'T GOING TO STEAL MY DETAILS?:
#     Because this script is in plain text and you can see all of the operations
#     carried out below these comments? Do you seriously think that I'd try and
#     steal your Gmail login details in such an obvious manner? Don't worry,
#     the email account linked to your level 80 Dark Elf with epic drops is
#     safe :P
#
#     I USE GOOGLE APPS, CAN I STILL USE THIS?:
#     Yes: Just enter your full Google Apps email address and password in the
#     email_user and email_pass values.
#
#     I WANT TO USE ANOTHER SMTP SERVER!:
#     Then just edit the smtp_server and smtp_port lines to match your SMTP
#     details.
#     I've attempted to add support for SMTP over SSL as well as Google's
#     default TLS option, but it's vastly untested. I've also not tested this
#     using plain old unsecure/unauthenticated SMTP, but I really wouldn't
#     advise using that anyway, and probably change to a better mail host if
#     they didn't offer some secure method of connecting.
#     If your mail provider only offers POP before SMTP authentication, then
#     there's not much I can do there for you.
#
#     YOUR PYTHON IS SHIT!:
#     That is not a question. And this is my first ever Python script. Blow me.

# Prints out usage instructions
def printUsage():
    print "USAGE:"
    print "  sendemail.py"
    print "  - Checks /mnt/sdcard/tmp/mailout.conf by default"
    print "  sendemail.py <conf file location>"
    print "  - Specify a conf file location"
    print "  sendemail.py <recipient> <subject> <message body>"
    print "  - Specify email details manually"

# Prints out an example conf file layout
def confFileLayout():
    print "EXAMPLE CONF FILE LAYOUT:"
    print "mailto: joe@bloggs.com"
    print "subject: This is the subject"
    print "body:"
    print "This is the body of the message."
    print "Note that the actual message begins AFTER the first line break after body:"
    print "Line breaks and spacing should be preserved by most mail clients."
    print "Most clients will also handle text wrapping automatically."
    print "This will be read all the way until the end of the file."

# Sends the actual email!
def sendemail(mailto,subject,body):
    import smtplib
    from .smtp.conf import email_name,email_user,email_pass

    # CHANGE THESE!
    # email_name = ' ' # Optional - A friendly name for the 'From' field
    # email_user = ' '
    # email_pass = ' '

    # DON'T CHANGE THIS!
    # ...unless you're rewriting this script for your own SMTP server!
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Build an SMTP compatible message from arguments
    if (email_name is not ''):
        msg = "From: " + email_name + " <" + email_user + ">\n"
    else:
        msg = "From: " + email_user + "\n"
    msg += "To: " + mailto + "\n"
    msg += "Subject: " + subject + "\n"
    msg += body

    # Attempt to connect and send the email!
    try:
        smtpObj = '' # Declare within this block.
        # Check for SMTP over SSL by port number and connect accordingly
        if( smtp_port == 465):
            smtpObj = smtplib.SMTP_SSL(smtp_server,smtp_port)
        else:
            smtpObj = smtplib.SMTP(smtp_server,smtp_port)
        smtpObj.ehlo()
        # StartTLS if using the default TLS port number
        if(smtp_port == 587):
            smtpObj.starttls()
            smtpObj.ehlo
        # Login, send and close the connection.
        smtpObj.login(email_user,email_pass)
        smtpObj.sendmail(email_user,mailto,msg)
        smtpObj.close()
        return 1  # Return 1 to denote success!
    except Exception, err:
        # Print error and return 0 on failure.
        print err
        return 0

import re,sys,math,os.path

# Declare variables...
conf_file = ''
mailto = ''
subject = ''
body = ''

# Check arg lengths and set up variables/conf file location accordingly
if ( len(sys.argv) == 4 ):
    # Pull out values if set individually
    mailto = sys.argv[1]

    # Check email address is valid!
    mailre = re.compile('(.+@.+\..+)',re.M)
    m = mailre.search(mailto)
    if(not m):
        print "Email recipient value " + mailto + " not a valid email address!"
        sys.exit(1)

    subject = sys.argv[2]
    body = sys.argv[3]
elif ( len(sys.argv) == 2 ):
    # If only one argument specified, assume conf file is specified
    conf_file = sys.argv[1]
else:
    # Otherwise, default to the following location
    conf_file = '/mnt/sdcard/tmp/mailout.conf'

# Process conf file if specified
if conf_file:
    if not os.path.isfile(conf_file):
        # Print out error and usage if specified conf file not found
        print "Unable to find file " + conf_file + "\n"
        printUsage()
        sys.exit(1)
    else:
        # Otherwise, read the file in and start processing!
        filein = open(str(conf_file),'r')
        mailconf = filein.read()

        # Check for valid email address in mailto field
        re1 = '^mailto: '
        re2 = '(.+@.+\..+)'
        re3 = '$'
        mailre = re.compile(re1+re2+re3,re.M)
        m = mailre.search(mailconf)
        if(m):
            mailto = m.group(1)
        else:
            mailto = ''

        # Grab subject from subject field...
        subjectre = re.compile('^subject: (.+)$',re.M)
        m = subjectre.search(mailconf)
        if(m):
            subject = m.group(1)
        else:
            subject = ''

        # And finally process the message body.
        bodyre = re.compile("body:\n(.+)", re.S)
        m = bodyre.search(mailconf)
        if(m):
            body = m.group(1)
        else:
            body = ''

        # Check all attributes were presen and valid.
        # Print out errors if anything missing!
        if ( mailto is '' or subject is '' or body is '' ):
            print "Unable to parse mail conf file"
            if (mailto is ''):
                print "mailto value is not present/not a valid email address"
            if (subject is ''):
                print "subject value is not present"
            if (body is ''):
                print "body value is not present"
            confFileLayout()
            sys.exit(1)


if ( mailto and subject and body ):
    # Send email if all values set!
    if (sendemail(mailto, subject, body)):
        print "Email sent successfully!"
        sys.exit(0)
    else:
        # Exit with error if email is not sent successfully
        print "Failed to send email! Check your login details and connection!"
        sys.exit(1)
else:
    # Print usage details if values not present.
    printUsage()
    sys.exit(1)
