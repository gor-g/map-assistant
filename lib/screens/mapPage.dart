import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:http/http.dart' as http;

class MapPage extends StatefulWidget {
  @override
  _MapPageState createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  late GoogleMapController mapController;

  final LatLng _center = const LatLng(45.640912263150796, 5.869377328664174);

  Set<Marker> markers = Set();

  void _onMapCreated(GoogleMapController controller) {
    mapController = controller;
    // Adding a sample marker for demonstration purposes
    markers.add(Marker(
      markerId: MarkerId('Marker1'),
      position: _center,
      infoWindow: InfoWindow(title: 'Sample Marker'),
      onTap: () {
        _sendLocationToServer(_center);
        print('Marker tapped! Place Name: Sample Marker');
      },
    ));
    setState(() {});
  }

  Future<void> _sendLocationToServer(LatLng location) async {
    var response = await http.post(
      Uri.parse('http://localhost:5000/location-clicked'),
      body: {'latitude': location.latitude.toString(), 'longitude': location.longitude.toString()},
    );

    if (response.statusCode == 200) {
      print('Location sent to server successfully.');
    } else {
      print('The server responded with error code : ${response.statusCode}'  );
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.green[700],
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('La fac'),
          elevation: 2,
        ),
        body: GoogleMap(
          onMapCreated: _onMapCreated,
          initialCameraPosition: CameraPosition(
            target: _center,
            zoom: 17.0,
          ),
          markers: markers,
          onTap: (LatLng location) {
            _sendLocationToServer(location);
            print('Tapped on location: $location');
          },
        ),
      ),
    );
  }
}
