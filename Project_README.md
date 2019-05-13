# XPorter

This project has had many names given the various pivots that we have made. The final iteration of the startup is entitled **XPorter** which is what you will see on final documents. Older documents will include the names: Semantic Vision (v1) and FoodPorter (v2).

## Product Narrative
XPorter leverages the power of remote driving to create a drive-on-demand system. With said system, users simply have to press a button to be connected to a XPorter operator. The operator will then verify the user’s credentials verbally then pass the destination information to a trained XPorter operator.

## Building The Architecture


### Streaming Video
Transporting the video to the driver was a essential task for us. In order to do this we started by downloading mjpg-streamer to the raspberry pi. mjpg-streamer is a command line tool specializing in copying JPEG frames from a input source, in this case the camera on the vehicle, to  output locations. Essentially, mjpg-streamer took our basic USB camera a made it a IP camera. The script in the driving files runs the following:

```
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so"
```

With this command we were able to forward all our video frames at the raspberry pi’s IP address. To video this on the web interface all we needed to do then was: 

```
 <img src="http://IP_ADDRESS_HERE:8080/?action=stream" />
```

#### AWS Solution
With Amazon Web Services, we were able to create a streamlined content distribution pipeline that allowed us to broadcast the vehicle’s live content to our remote drivers. The significance of building a pipeline on top of AWS services is we were able to easily scale our infrastructure as demand increased. Unlike our first streaming solution, we were able to create a more reliable stream that can be viewed by more than one person at time. 

Our streaming solution is a combination of AWS Media Services with Amazon CloudFront to offer a more secure architecture. The camera attached to the vehicle acts as a producer: which is an video-generating device. We have the single producer generating one video stream that includes just the raw video frames. It is possible to have a single producer push two streams at one time, but in our case audio wasn’t necessary. However, if we wanted to bring the startup to life we would definitely choose to use audio as a means of increasing safety.

We then take each of the frames and have them pushed to a Kinesis video stream. The Kinesis video stream transports live video data, stores it in a S3, and then makes it available for real time viewing. This process is done programmatically using the AWS SDKs (e.g. C++ Producer SDK). The entire process is managed by the AWS Console.

Setting up our client (File on Raspberry Pi):
```
<script src="https://cdnjs.cloudflare.com/ajax/libs/aws-sdk/2.278.1/aws-sdk.min.js"></script>

var streamName = ‘XPorter’;

// Step 1: Configure SDK Clients
var options = {
    accessKeyId: 'ACCESS_KEY_ID',
    secretAccessKey: 'SECRET_KEY',
    region: 'us-east-1'
}
var kinesisVideo = new AWS.KinesisVideo(options);
var kinesisVideoArchivedContent = new AWS.KinesisVideoArchivedMedia(options);
```

Getting the streams endpoint
```
kinesisVideo.getDataEndpoint({
    StreamName: streamName,
    APIName: "GET_HLS_STREAMING_SESSION_URL"
}, function(err, response) {
    if (err) { return console.error(err); }
    console.log('Data endpoint: ' + response.DataEndpoint);
    kinesisVideoArchivedContent.endpoint = new AWS.Endpoint(response.DataEndpoint);
});
```
With the previous two code blocks we were able to start streaming and collect the url endpoint. Having the url end point made it possible for us to inject the live stream into our website interface. This had to be done with the [Video.js](https://github.com/videojs/video.js/) library.

### Security Management Video
Our first approach was to just use as standard IP camera to get the video to the web interface. The problem with this method is that IP cameras are among the most common causes of security breaches. Choosing to go with route makes it painfully easy for a hacker to in the best case to capture the video and in the worst case get completely into the system. Adding the video streaming password provided some support by the AWS approach did much more.

With AWS we were provided with the following protections (many of which needed to be turned on and were):
* detailed control over the instance the video stream was running on
* encryption in transit with TLS across all services
* Automatic encryption of all traffic on the AWS global and regional networks between AWS secured facilities 
* AWS Key management services so only uses who needed access have it
* Deployment tools that allowed us to erase all video frames once the stream was completed
* Log aggregation options, streamlining investigations and compliance reporting
