
// Initialize the Cesium viewer.
const viewer = new Cesium.Viewer('cesiumContainer', {
    imageryProvider: new Cesium.TileMapServiceImageryProvider({
        url: Cesium.buildModuleUrl("Assets/Textures/NaturalEarthII"),
    }),
    baseLayerPicker: false, geocoder: false, homeButton: false, infoBox: false,
    navigationHelpButton: false,
});

var l1 = document.getElementsByClassName("l1").value
var l2 = document.getElementsByClassName("l2").value


const satrec = satellite.twoline2satrec(
    l1.trim(),
    l2.trim()
);

// We're going to generate a position every 10 seconds from now until 6 seconds from now. 
const totalSeconds = 60 * 60 * 6;
const timestepInSeconds = 10;
const start = Cesium.JulianDate.fromDate(new Date());
const stop = Cesium.JulianDate.addSeconds(start, totalSeconds, new Cesium.JulianDate());
viewer.clock.startTime = start.clone();
viewer.clock.stopTime = stop.clone();
viewer.clock.currentTime = start.clone();
viewer.timeline.zoomTo(start, stop);
viewer.clock.multiplier = 40;
viewer.clock.clockRange = Cesium.ClockRange.LOOP_STOP;


const positionsOverTime = new Cesium.SampledPositionProperty();
for (let i = 0; i < totalSeconds; i += timestepInSeconds) {
    const time = Cesium.JulianDate.addSeconds(start, i, new Cesium.JulianDate());
    const jsDate = Cesium.JulianDate.toDate(time);

    const positionAndVelocity = satellite.propagate(satrec, jsDate);
    const gmst = satellite.gstime(jsDate);
    const p = satellite.eciToGeodetic(positionAndVelocity.position, gmst);

    const position = Cesium.Cartesian3.fromRadians(p.longitude, p.latitude, p.height * 1000);
    positionsOverTime.addSample(time, position);
}


// Visualize the satellite with a red dot.
const satellitePoint = viewer.entities.add({
    position: positionsOverTime,
    point: { pixelSize: 5, color: Cesium.Color.RED }
});

// Set the camera to follow the satellite 
viewer.trackedEntity = satellitePoint;

// Wait for globe to load then zoom out     
let initialized = false;
viewer.scene.globe.tileLoadProgressEvent.addEventListener(() => {
    if (!initialized && viewer.scene.globe.tilesLoaded === true) {
        viewer.clock.shouldAnimate = true;
        initialized = true;
        viewer.scene.camera.zoomOut(7000000);
        document.querySelector("#loading").classList.toggle('disappear', true)
    }
});
