'use strict';
import * as vscode from 'vscode';
//import {workspace, window, TextDocument, Uri, CancellationToken} from 'vscode';
import { AppInsightsClient } from './appInsightsClient';

export function activate(context: vscode.ExtensionContext) {

    let disposable = vscode.commands.registerCommand('extension.openChatRoom', () => {

        const panel = vscode.window.createWebviewPanel("chatRoom", "Botlearn", vscode.ViewColumn.Two, {
            enableScripts: true,
            retainContextWhenHidden: true,
        });
        
        panel.webview.html = `
        <body style="margin:0px;padding:0px;overflow:hidden">
          <iframe id="botFrame" src="https://memoire-bot.jacquant.be/login" frameborder="0" 
          style="overflow:hidden;overflow-x:hidden;overflow-y:hidden;height:100%;width:100%;position:absolute;
          top:0px;left:0px;right:0px;bottom:0px" height="20%" width="100%">
          </iframe>
          
          <center id="loadingMessage">
            <div class="loader"></div>
            <h1> En cours de chargement ! </h1>
            <h1 id="ErrorMessageNoInternet" style="display:none; color:red; "> Le chabot n'arrive pas à charger ! 
            Merci de vérifier ta connexion internet. </h1>
            <h1 id="ErrorMessageIframeNotLoading" style="display:none; color:red; "> Le chabot n'arrive à charger ! 
            Merci de ré-essayer plus tard. </h1>
          </center>

          <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
          <script>

          //Not using Jquerry to show this message because without internet, Jquery is not loaded as well
          if (!navigator.onLine) {
            document.getElementById("ErrorMessageNoInternet").style.display = 'block';
          }

          //If Iframe is loaded correctly, removing message
          $('#botFrame').on('load',function () {
            $('#loadingMessage').css('display', 'none');
          });

         
            
     

          //Define vscode to communicate between WebView and the Extension
          const vscode = acquireVsCodeApi();


          $(function () {  
              $("#botFrame").on("load", function () {                        
                  var window = document.getElementById("botFrame").contentWindow;
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
                  window.postMessage({code: evt.data.code, filename: evt.data.filename}, '*');
                }
              }

              if (window.addEventListener) {
                window.addEventListener("message", manageRequests, false);  
              }
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

      .loader {
        border: 16px solid #f3f3f3;
        border-radius: 50%;
        border-top: 16px solid #3498db;
        width: 60px;
        height: 60px;
        animation: spin 2s linear infinite;
      }
      
      @-webkit-keyframes spin {
        0% { -webkit-transform: rotate(0deg); }
        100% { -webkit-transform: rotate(360deg); }
      }
      
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      
      </style>`;
      let currentTabOpen:any;
      
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
              panel.webview.postMessage({code: currentTabOpen.document.getText(), 
                                        filename: currentTabOpen.document.fileName});
              return ;

            }else{
              vscode.window.showErrorMessage("Aucun code n'est ouvert actuellement ! ");
            }
          }
        },
        undefined,
        context.subscriptions
      );


    AppInsightsClient.sendEvent("openChatRoom");
    });

    const chatRoomStatusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 9999);
    chatRoomStatusBarItem.command = "extension.openChatRoom";
    chatRoomStatusBarItem.text = "$(comment-discussion) ChatBot";
    chatRoomStatusBarItem.tooltip = "Ouvrir le ChatBot";
    chatRoomStatusBarItem.show();

    context.subscriptions.push(disposable);
}

export function deactivate() {
}

export function getCurrentTabOpen() {

    return null;
}