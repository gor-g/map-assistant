import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatPage extends StatefulWidget {
  @override
  _ChatPageState createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  TextEditingController _messageController = TextEditingController();
  List<Map<String, String>> _chatMessages = [];
  late ScrollController _scrollController;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
    fetchConversationHistory();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void fetchConversationHistory() async {
    final response = await http.get(Uri.parse('http://localhost:5000/conversation-history'));

    if (response.statusCode == 200) {
      List<dynamic> history = json.decode(response.body);
      setState(() {
        _chatMessages.clear();
        for (var item in history) {
          _chatMessages.add({'sender': 'You', 'message': item['user']});
          _chatMessages.add({'sender': 'Bot', 'message': item['assistant']});
        }
      });
      _scrollToBottom(); // Scroll to the bottom after loading history
    } else {
      // Handle server communication error
    }
  }

  void _scrollToBottom() {
    _scrollController.animateTo(
      _scrollController.position.maxScrollExtent,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeOut,
    );
  }

  void _sendMessage(String message) async {
    final response = await http.post(
      Uri.parse('http://localhost:5000/send-message'),
      body: {'message': message},
    );

    if (response.statusCode == 200) {
      Map<String, dynamic> data = json.decode(response.body);
      String botResponse = data['response'];
      setState(() {
        _chatMessages.add({'sender': 'You', 'message': message});
        _chatMessages.add({'sender': 'Bot', 'message': botResponse});
      });
      _scrollToBottom(); // Scroll to the bottom after adding a new message
    } else {
      // Handle server communication error
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chat with Bot'),
      ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              itemCount: _chatMessages.length,
              itemBuilder: (context, index) {
                final isUserMessage = _chatMessages[index]['sender'] == 'You';

                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
                  child: Row(
                    mainAxisAlignment: isUserMessage
                        ? MainAxisAlignment.end
                        : MainAxisAlignment.start,
                    children: [
                      Flexible(
                        child: Container(
                          padding: EdgeInsets.all(12.0),
                          decoration: BoxDecoration(
                            color: isUserMessage ? Colors.blue : Colors.green,
                            borderRadius: isUserMessage
                                ? BorderRadius.only(
                              topLeft: Radius.circular(8.0),
                              topRight: Radius.circular(8.0),
                              bottomLeft: Radius.circular(8.0),
                              bottomRight: Radius.circular(0.0),
                            )
                                : BorderRadius.only(
                              topLeft: Radius.circular(8.0),
                              topRight: Radius.circular(8.0),
                              bottomLeft: Radius.circular(0.0),
                              bottomRight: Radius.circular(8.0),
                            ),
                          ),
                          child: Wrap(
                            children: [
                              Text(
                                _chatMessages[index]['message'] ?? 'Received null message',
                                style: TextStyle(color: Colors.white),
                                softWrap: true,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: <Widget>[
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'Type your message...',
                    ),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: () {
                    String message = _messageController.text;
                    if (message.isNotEmpty) {
                      _sendMessage(message);
                      _messageController.clear();
                    }
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
