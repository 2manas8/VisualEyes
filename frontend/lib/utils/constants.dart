// Duration constants
const Duration splashScreenDuration = Duration(seconds: 2);
const Duration networkSwitchDelay = Duration(seconds: 5);

// Image constants
const String logo = 'assets/images/logo.png';

// Padding, margin and radius constants
const double defaultPadding = 16.0;
const double defaultMargin = 8.0;
const double defaultBorderRadius = 20.0;

// Text constants
const String detectText = 'Detect';
const String descriptionText = 'Description';
const String connectText = 'Connect';
const String wifiSsidText = 'Enter WiFi SSID';
const String wifiPasswordText = 'Enter WiFi password';
const String retryText = 'Retry';

// API constants
const String apiBaseUrl = 'https://visualeyes.onrender.com/api';
const String latestFrameEndpoint = '/detect/latest_frame';
const String socketUrl = 'https://visualeyes.onrender.com';
const String wifiUrl = 'http://192.168.4.1/set';

// Header constants
const Map<String, String> apiHeader = {"Content-Type" : "application/json"};