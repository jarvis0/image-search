# typing-assistant
Codebase for a question auto-completion proof of concept.
Research is available on [Confluence](https://igenius.atlassian.net/wiki/spaces/CF/pages/1919025801/Question+auto-completion+Research).

### Experimental
![](demo.gif)

In addition to question auto-completion which provides _long-term_ predictions of full sentences, this code will also provide (upon tab keybutton press):
- word auto-correction highlighted in green on the second row if a typo is detected (after a space);
- word auto-completion highlighted in dim black on the second row if a word completion is available;
- next word prediction highlighted in dim black on the same row of the query if a prediction for the next word is available (after a space).
