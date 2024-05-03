import 'dart:async';

import '../components/clock_view.dart';
import '../ui/colors.dart';
import '../utils/time.dart';
import 'package:flutter/material.dart';
import 'package:timer_builder/timer_builder.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  HomePageState createState() => HomePageState();
}

class HomePageState extends State<HomePage> {
  DateTime now = DateTime.now();
  Timer? _everySec;

  DateTime? alarmTime;

  Future<DateTime> fetchClock() async {
    now = DateTime.now();
    return now;
  }

  @override
  void initState() {
    super.initState();

    _everySec = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        now = DateTime.now();
        if (alarmTime != null &&
            now.hour == alarmTime!.hour &&
            now.minute == alarmTime!.minute &&
            now.second == alarmTime!.second) {
          _showAlarmDialog(context);
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFfafafa),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              TimerBuilder.periodic(
                const Duration(seconds: 1),
                builder: (context) {
                  String second = DateTime.now().second < 10
                      ? "0${DateTime.now().second}"
                      : DateTime.now().second.toString();
                  String minute = DateTime.now().minute < 10
                      ? "0${DateTime.now().minute}"
                      : DateTime.now().minute.toString();
                  String hour = DateTime.now().hour < 10
                      ? "0${DateTime.now().hour}"
                      : DateTime.now().hour.toString();
                  return Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "$hour:$minute:$second",
                            style: AppStyle.mainText,
                          ),
                        ],
                      ),
                      const SizedBox(
                        height: 40.0,
                      ),
                      ClockView(DataTime(DateTime.now().hour,
                          DateTime.now().minute, DateTime.now().second)),
                    ],
                  );
                },
              ),
              ElevatedButton(
                onPressed: () => _showAlarmTimePicker(context),
                style: ButtonStyle(
                  minimumSize: MaterialStateProperty.resolveWith<Size>(
                        (Set<MaterialState> states) {
                      final width = MediaQuery.of(context).size.width * 0.5;
                      final height = MediaQuery.of(context).size.height * 0.06;
                      return Size(width, height);
                    },
                  ),
                  backgroundColor: MaterialStateProperty.all<Color>(const Color(0xFF2253FF)),
                  foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
                  shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                    RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8.0),
                    ),
                  ),
                ),
                child: const Text('Set Alarm'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showAlarmTimePicker(BuildContext context) async {
    final selectedTime = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.fromDateTime(DateTime.now()),
      builder: (BuildContext context, Widget? child) {
        return Theme(
          data: ThemeData(
            colorScheme: const ColorScheme.light(
              primary: Color(0xFF2253FF),
              onPrimary: Colors.white,
              surface: Colors.white
            ),
            dialogBackgroundColor: Colors.white,
          ),
          child: child!,
        );
      },
    );

    if (selectedTime != null) {
      setState(() {
        alarmTime = DateTime(now.year, now.month, now.day, selectedTime.hour, selectedTime.minute);
      });
    }
  }

  void _showAlarmDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Alarm', style: TextStyle(color: Color(0xFF2253FF))),
          content: const Text('Time to wake up!', style: TextStyle(color: Color(0xFF193BB1))),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
  }
}
