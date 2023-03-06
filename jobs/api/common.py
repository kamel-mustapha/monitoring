import json, time, requests
from api.models import *
from background_task import background
from django.core.mail import send_mail


# logging
from logging import getLogger
logger = getLogger(__name__)


status_messages_long = {
    100: "This interim response indicates that the client should continue the request or ignore the response if the request is already finished.",
    101: "This code is sent in response to an Upgrade request header from the client and indicates the protocol the server is switching to.",
    102: "This code indicates that the server has received and is processing the request, but no response is available yet.",
    103: "This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response.",
    200: "The request succeeded.",
    201: "The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests.",
    202: "The request has been received but not yet acted upon.",
    203: "This response code means the returned metadata is not exactly the same as is available from the origin server, but is collected from a local or a third-party copy.",
    204: "There is no content to send for this request, but the headers may be useful.",
    205: "Tells the user agent to reset the document which sent this request.",
    206: "This response code is used when the Range header is sent from the client to request only part of a resource.",
    207: "Conveys information about multiple resources, for situations where multiple status codes might be appropriate.",
    208: "Used inside a <dav:propstat> response element to avoid repeatedly enumerating the internal members of multiple bindings to the same collection.",
    226: "The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance.",
    300: "The request has more than one possible response. The user agent or user should choose one of them. ",
    301: "The URL of the requested resource has been changed permanently. The new URL is given in the response.",
    302: "This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future.",
    303: "The server sent this response to direct the client to get the requested resource at another URI with a GET request.",
    304: "This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response.",
    305: "Defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy. It has been deprecated due to security concerns regarding in-band configuration of a proxy.",
    306: "This response code is no longer used; it is just reserved. It was used in a previous version of the HTTP/1.1 specification.",
    307: "The server sends this response to direct the client to get the requested resource at another URI with same method that was used in the prior request.",
    308: "This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header.",
    400: "The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing).",
    401: 'Although the HTTP standard specifies "unauthorized", semantically this response means "unauthenticated". That is, the client must authenticate itself to get the requested response.',
    402: "This response code is reserved for future use. The initial aim for creating this code was using it for digital payment systems, however this status code is used very rarely and no standard convention exists.",
    403: "The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource.",
    404: "The server cannot find the requested resource.",
    405: "The request method is known by the server but is not supported by the target resource. For example, an API may not allow calling DELETE to remove a resource.",
    406: "This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent.",
    407: "This is similar to 401 Unauthorized but authentication is needed to be done by a proxy.",
    408: "This response is sent on an idle connection by some servers, even without any previous request by the client.",
    409: "This response is sent when a request conflicts with the current state of the server.",
    410: "This response is sent when the requested content has been permanently deleted from server, with no forwarding address.",
    411: "Server rejected the request because the Content-Length header field is not defined and the server requires it.",
    412: "The client has indicated preconditions in its headers which the server does not meet.",
    413: "Request entity is larger than limits defined by server. The server might close the connection or return an Retry-After header field.",
    414: "The URI requested by the client is longer than the server is willing to interpret.",
    415: "The media format of the requested data is not supported by the server, so the server is rejecting the request.",
    416: "The range specified by the Range header field in the request cannot be fulfilled. It's possible that the range is outside the size of the target URI's data.",
    417: "This response code means the expectation indicated by the Expect request header field cannot be met by the server.",
    418: "The server refuses the attempt to brew coffee with a teapot.",
    421: "The request was directed at a server that is not able to produce a response. This can be sent by a server that is not configured to produce responses for the combination of scheme and authority that are included in the request URI.",
    422: "The request was well-formed but was unable to be followed due to semantic errors.",
    423: "The resource that is being accessed is locked.",
    424: "The request failed due to failure of a previous request.",
    425: "Indicates that the server is unwilling to risk processing a request that might be replayed.",
    426: "The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol.",
    428: "The origin server requires the request to be conditional. This response is intended to prevent the 'lost update' problem, where a client GETs a resource's state, modifies it and PUTs it back to the server, when meanwhile a third party has modified the state on the server, leading to a conflict.",
    429: 'The user has sent too many requests in a given amount of time ("rate limiting").',
    431: "The server is unwilling to process the request because its header fields are too large. The request may be resubmitted after reducing the size of the request header fields.",
    451: "The user agent requested a resource that cannot legally be provided, such as a web page censored by a government.",
    500: "The server has encountered a situation it does not know how to handle.",
    501: "The request method is not supported by the server and cannot be handled. The only methods that servers are required to support (and therefore that must not return this code) are GET and HEAD.",
    502: "This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response.",
    503: "The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded.",
    504: "This error response is given when the server is acting as a gateway and cannot get a response in time.",
    505: "The HTTP version used in the request is not supported by the server.",
    506: "The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself, and is therefore not a proper end point in the negotiation process.",
    507: "The method could not be performed on the resource because the server is unable to store the representation needed to successfully complete the request.",
    508: "The server detected an infinite loop while processing the request.",
    510: "Further extensions to the request are required for the server to fulfill it.",
    511: "Indicates that the client needs to authenticate to gain network access."
}

status_messages = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    208: "Already Reported",
    226: "IM Used",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "unused",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: 'Unauthorized',
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: 'Too Many Requests',
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required"
}


def send_alert_email(alert_emails, monitor_link, status, downtime=None, success=False):
    try:
        if success:
            message = f"Your monitor {monitor_link} is up again, good job."
            if downtime:
                message += f"<br><div>Downtime: {downtime}</div>"
            send_mail(
                'MONITOR UP',
                'Your monitor is up again',
                'musk96.km@gmail.com',
                alert_emails,
                fail_silently=False,
                html_message=message
            )
        else:
            message = f"<div>Your monitor {monitor_link} went down with a status of {status}.</div><div>{status_messages_long.get(status)}</div>"
            send_mail(
                'MONITOR DOWN',
                'Your monitor went down',
                'musk96.km@gmail.com',
                alert_emails,
                fail_silently=False,
                html_message=message
            )
    except Exception as e:
        logger.exception(e)
  
@background
def monitor_http(monitor_id, monitor_link, success_status, timeout, alert_emails):
    status = 404
    request_time = 0
    is_success = False
    failure_start = False
    failure_end = False
    last_event = MonitorEvent.objects.all().order_by("-id")[:1]
    try:
        logger.info(f"Started monitoring {monitor_id}")
        start = time.time()
        r = requests.get(monitor_link, timeout=timeout)
        end = time.time()
        status = r.status_code
        request_time = (end-start)*1000
        if status == success_status:
            is_success = True
            if last_event and not last_event[0].is_success:
                failure_end = True
                downtime_start = MonitorEvent.objects.filter(failure_start=True).order_by("-id")[0]
                send_alert_email(alert_emails, monitor_link, status, downtime=last_event[0].created_time-downtime_start.created_time, success=True)
        elif status != success_status and last_event and last_event[0].is_success:
            failure_start = True
            send_alert_email(alert_emails, monitor_link, status)
    except Exception as e:
        status = 404
        is_success = False
        end = time.time()
        request_time = (end-start)*1000
        if last_event and last_event[0].is_success:
            failure_start = True
        logger.exception(e)
        
    MonitorEvent.objects.create(
        monitor_id=monitor_id,
        status=status,
        time=request_time,
        message=status_messages.get(status),
        is_success=is_success,
        failure_start=failure_start,
        failure_end=failure_end
    )