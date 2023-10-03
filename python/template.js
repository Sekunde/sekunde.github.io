function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 2,
    center: { lat: 30.0, lng: 0.0 },
  });

  const infoWindow = new google.maps.InfoWindow({
    content: "",
    disableAutoPan: true,
  });

  var template = [
                '<?xml version="1.0"?>',
                '<svg fill="{{color}}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">',
                '<circle cx="120" cy="120" opacity=".6" r="70" />',
                '<circle cx="120" cy="120" opacity=".3" r="90" />',
                '<circle cx="120" cy="120" opacity=".2" r="110" />',
                '</svg>'].join('\n');
    var svg_icon = template.replace('{{color}}', '#0000ff');

    const markers = locations.map((data) => {
    const position = {lat: data.Latitude, lng:data.Longtitude};
    const title = "<em>" + data.title + "</em></br></br>" + "<b>Institue:</b> " + data.Institute + "</br><b>Position: </b>" + data.Latitude + "," + data.Longtitude;
    const marker = new google.maps.Marker({
      position,
      label: {text:String(1),color:"rgba(255,255,255,0.9)",fontSize:"12px" },
      icon:{url:"data:image/svg+xml;base64," + btoa(svg_icon),scaledSize:new google.maps.Size(45,45)},
    });

    // markers can only be keyboard focusable when they have click listeners
    // open info window when marker is clicked
    marker.addListener("click", () => {
      infoWindow.setContent(title);
      infoWindow.open(map, marker);
    });
    return marker;});

    new markerClusterer.MarkerClusterer({ markers, map });

}
