'use strict';
import * as vscode from 'vscode';
import {window} from 'vscode'
//import {workspace, window, TextDocument, Uri, CancellationToken} from 'vscode';
import { AppInsightsClient } from './appInsightsClient';

export function activate(context: vscode.ExtensionContext) {

    let disposable = vscode.commands.registerCommand('extension.openChatRoom', () => {

        const panel = vscode.window.createWebviewPanel("chatRoom", "Chat Room", vscode.ViewColumn.Two, {
            enableScripts: true,
            retainContextWhenHidden: true,
        });
        
        panel.webview.html = `
        <body style="margin:0px;padding:0px;overflow:hidden">
          <button id="run" style="background-color: #4CAF50;border: none;color: white;padding: 15px 32px;text-align: center;
                          text-decoration: none;display: inline-block;font-size: 16px;justify-content: center;position:absolute;">
          TEST </button>
          <iframe id="botFrame" src="http://localhost:3001/bot" frameborder="0" 
          style="overflow:hidden;overflow-x:hidden;overflow-y:hidden;height:100%;width:100%;position:absolute;
          top:0px;left:0px;right:0px;bottom:0px" height="20%" width="100%">
          </iframe>

          <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
          <script>

          //Define vscode to communicate between WebView and the Extension
          const vscode = acquireVsCodeApi();


          $(function () {  
              $("#botFrame").on("load", function () {                        
                  var window = document.getElementById("botFrame").contentWindow;
                  window.postMessage({message: 'Hello world'}, '*');
                  //setInterval(function(){ window.postMessage({message: 'Hello world'}, '*'); }, 3000);
                  //console.log($('#botFrame').get(0).contentWindow.document)
              });
          }); 

              //Managing the CORS Requets
              let currentTab = null;
              function manageRequests (evt) {

                //Sending a message to get the code in the extension
                if(evt.data == 'run'){
                  vscode.postMessage({
                    command: 'run'
                  })

                //Sending the code entered by the user
                }else if (evt.data.code !== undefined){
                  var window = document.getElementById("botFrame").contentWindow;
                  window.postMessage({code: evt.data.code}, '*');
                }
              }

              if (window.addEventListener) {
                window.addEventListener("message", manageRequests, false);  
              }
              

              $("#run").click( function(){
                  var window = document.getElementById("botFrame").contentWindow;
                  let data_request = '{"text":"'+ String("coucou") + '"}'
                  window.postMessage({message: 'Hello world'}, '*');
              });
          </script>
      </body>

      <style>
          .button {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
      }
      </style>`;
      let currentTabOpen;
      /*Getting data if button run is pressed in the iframe
      
      vscode.window.onDidChangeActiveTextEditor(
        function(currentTab){
          documentOpen = currentTab;
        }
        
        );*/
      
      //vscode.window.onDidChangeActiveTextEditor(event =>{console.log(event);});

      //Getting the Exercice if it is already opened
       
      //Save the last Python tab opened
      if(vscode.window.activeTextEditor!== undefined && vscode.window.activeTextEditor.document.languageId === "python"){
        currentTabOpen = vscode.window.activeTextEditor;
      }
      vscode.window.onDidChangeActiveTextEditor(
        function(currentTab){
          if(currentTab!== undefined && currentTab.document.languageId === "python"){
            currentTabOpen = currentTab;
          }
      });

      panel.webview.onDidReceiveMessage( message => {
          if(message.command === "run"){
            if(currentTabOpen !== undefined){
              console.log("Sending code to the website");
              panel.webview.postMessage({code: currentTabOpen.document.getText()});
              return ;

            }else{
              vscode.window.showErrorMessage("Aucun code n'est ouvert actuellement ! ");
            }
          }
        },
        undefined,
        context.subscriptions
      );

      //setInterval(function(){console.log(message);},2000);
      //message.watch( "message", function(){console.log(message);});

        //console.log(vscode.window.activeTextEditor);
        //console.log(getCurrentTabOpen());
        //if(vscode.window.activeTextEditor !== undefined){
        
        //console.log(vscode.window.activeTextEditor.document.getText());
      //}

        /*vscode.window.onDidChangeActiveTextEditor(function(){
            console.log(vscode.window.activeTextEditor.document.getText());
        
        });*/

      


    AppInsightsClient.sendEvent("openChatRoom");
    });

    const chatRoomStatusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 9999);
    chatRoomStatusBarItem.command = "extension.openChatRoom";
    chatRoomStatusBarItem.text = "$(comment-discussion) Chat";
    chatRoomStatusBarItem.tooltip = "Open Chat Room";
    chatRoomStatusBarItem.show();

    context.subscriptions.push(disposable);
}

export function deactivate() {
}

export function getCurrentTabOpen() {

    return null;
}