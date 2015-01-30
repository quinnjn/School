<?php
require 'globals.php';
require 'oauth_helper.php';

// Callback can either be 'oob' or a url
$callback='oob';

#You can either get these two values from globals.php or via the command line
#To get them from globals.php, leave these next two lines uncommented
#And leave the two lines ending in argv[1] and argv[2] commented out
$oauth_consumer_key = "iFxEvQPiL93bW170pFgu0g";
$oauth_consumer_secret = "kJsLUrTJ6BUCUepE300RGvgRtSe8jfYQximND0gLUc";
#To get the values from arguments, uncomment the next two lines
#And comment out the two lines above with OAUTH_CONSUMER_KEY AND OAUTH_CONSUMER_SECRET
// $oauth_consumer_key=$argv[1];
// $oauth_consumer_secret=$argv[2];

// Get the request token using HTTP GET and HMAC-SHA1 signature
$retarr = get_request_token($oauth_consumer_key, $oauth_consumer_secret,
                            $callback, false, true, true);
if (! empty($retarr)) {
  list($info, $headers, $body, $body_parsed) = $retarr;
  $oauth_token=($body_parsed[oauth_token]);
  $oauth_token_secret=($body_parsed[oauth_token_secret]);
  if ($info['http_code'] == 200 && !empty($body)) {
    print "\n1. Login to twitter.com as the user you want to send automated tweets from.\n2. Point web browser to the following URL:\n\n" .
        "http://api.twitter.com/oauth/authorize?" .
        rfc3986_decode($body) . "\n";
    print "\n3. Click on \"Authorize App\" at twitter.com and observe the value it gives you.\n4. Replace [AUTHKEY] in the following command with the value that twitter gives you:\n\nphp getacctok.php $oauth_consumer_key $oauth_consumer_secret $oauth_token $oauth_token_secret [AUTHKEY]\n\n";
  }
}

exit(0);

/**
 * Get a request token.
 * @param string $consumer_key obtained when you registered your app
 * @param string $consumer_secret obtained when you registered your app
 * @param string $callback callback url can be the string 'oob'
 * @param bool $usePost use HTTP POST instead of GET
 * @param bool $useHmacSha1Sig use HMAC-SHA1 signature
 * @param bool $passOAuthInHeader pass OAuth credentials in HTTP header
 * @return array of response parameters or empty array on error
 */
function get_request_token($consumer_key, $consumer_secret, $callback, $usePost=false, $useHmacSha1Sig=true, $passOAuthInHeader=false)
{
  $retarr = array();  // return value
  $response = array();

  $url = 'http://api.twitter.com/oauth/request_token';
  $params['oauth_version'] = '1.0';
  $params['oauth_nonce'] = mt_rand();
  $params['oauth_timestamp'] = time();
  $params['oauth_consumer_key'] = $consumer_key;
  $params['oauth_callback'] = $callback;

  // compute signature and add it to the params list
  if ($useHmacSha1Sig) {
    $params['oauth_signature_method'] = 'HMAC-SHA1';
    $params['oauth_signature'] =
      oauth_compute_hmac_sig($usePost? 'POST' : 'GET', $url, $params,
                             $consumer_secret, null);
  } else {
    $params['oauth_signature_method'] = 'PLAINTEXT';
    $params['oauth_signature'] =
      oauth_compute_plaintext_sig($consumer_secret, null);
  }

  // Pass OAuth credentials in a separate header or in the query string
  if ($passOAuthInHeader) {
    $query_parameter_string = oauth_http_build_query($params, true);
    $header = build_oauth_header($params, "Twitter API");
    $headers[] = $header;
  } else {
    $query_parameter_string = oauth_http_build_query($params);
  }

  // POST or GET the request
  if ($usePost) {
    $request_url = $url;
    logit("getreqtok:INFO:request_url:$request_url");
    logit("getreqtok:INFO:post_body:$query_parameter_string");
    $headers[] = 'Content-Type: application/x-www-form-urlencoded';
    $response = do_post($request_url, $query_parameter_string, 80, $headers);
  } else {
    $request_url = $url . ($query_parameter_string ?
                           ('?' . $query_parameter_string) : '' );
    logit("getreqtok:INFO:request_url:$request_url");
    $response = do_get($request_url, 80, $headers);
  }

  // extract successful response
  if (! empty($response)) {
    list($info, $header, $body) = $response;
    $body_parsed = oauth_parse_str($body);
    if (! empty($body_parsed)) {
      logit("getreqtok:INFO:response_body_parsed:");
      #print_r($body_parsed);
    }
    $retarr = $response;
    $retarr[] = $body_parsed;
  }

  return $retarr;
}
?>
