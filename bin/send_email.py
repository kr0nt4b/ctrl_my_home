#!/usr/bin/python
import smtplib
import sys
from optparse import OptionParser
from os.path import basename

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# *************************************************************************** #
# Constants.
# *************************************************************************** #
NAGIOS_CODES = {"UNKNOWN": -1,
                "OK": 0,
                "WARNING": 1,
                "CRITICAL": 2,
                "DEPENDENT": 4}

# *************************************************************************** #
#   _nagiosReturn
#
def nagiosReturn(code, response):
    """ Prints the response message
        and exits the script with one
        of the defined exit codes

        return  DOES NOT RETURN
    """
    print code + ": " + response

    sys.exit(NAGIOS_CODES[code])


def _parseArgs():
    """ Handles parsing of arguments using optparse.OptionParser.
        It makes command-line args a breeze, and generates auto "-h" text.

        return  the options
    """
    usage = "usage: %prog -f  <from> -t <to> -s <subject> -m <message> [ -c ]"

    parser = OptionParser(usage = usage)
    parser.add_option("-f", "--from", dest="fromaddr",
                      help="from address (eg. nagios.systeembeheer@technolution.nl)")
    parser.add_option("-t", "--to", dest="to",
                      help="to address (eg support@technolution.nl")
    parser.add_option("-s", "--subject", dest="subject",
                      help="subject (eg \"how are you?\" ")
    parser.add_option("-m", "--message", dest="message",
                      help="plaintext message")
    parser.add_option("-c", "--just-check", action="store_true", dest="check",
                      help="just check if connecting to gmail is possible (i.e. check credentials)")
    parser.add_option("-i", "--files", dest="files",
                      help="just check if connecting to gmail is possible (i.e. check credentials)")

    options, args = parser.parse_args()

    # Check for required options
    for option in ("fromaddr", "to", "subject"):
        if not getattr(options, option):
            print "option --%s not specified" % (option)
            sys.exit(-1)

    if getattr(options,'files'):
        options.files = options.files.split(',') 
    else:
        filesSplit = []

    return options

def main():

    options = _parseArgs()
    
    sent_from = options.fromaddr
    sent_to  = options.to
    body = options.message
    subject = options.subject
    check = not options.check
    filesSplit = options.files

    msg = MIMEMultipart()
    msg['From'] = sent_from
    msg['To'] = sent_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    for f in filesSplit or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f),
                Name=basename(f)
            ))

    
    # Credentials (if needed)
    username = 'random.klaus@gmail.com'
    #password = 'uxvgqovmruccemcs'
    password = 'nuklmtplysgkprsw '
    # The actual mail send
    server = smtplib.SMTP_SSL('smtp.gmail.com:465')

    try:
        server.login(username,password)
        if check:
            server.sendmail(sent_from, sent_to, msg.as_string())
        server.quit()
    except smtplib.SMTPAuthenticationError:
        sys.exit(2)
    
    sys.exit(0)

if __name__ == "__main__":
    main()

