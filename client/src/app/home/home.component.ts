import { Component } from '@angular/core';
import {ConnectionService} from "../connection.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  host: string = 'localhost';
  port: string = '9000';
  pattern: File;
  source: File;

  constructor(private service: ConnectionService) {
  }

  setPort(value) {
    this.port = value;
  }

  setHost(value) {
    this.host = value;
  }

  setSource(value) {
    this.source = value;
  }

  setPattern(value) {
    this.pattern = value;
  }

  send() {
    this.service.connectAndSend(this.host, this.port, this.source, this.pattern);
  }

}
