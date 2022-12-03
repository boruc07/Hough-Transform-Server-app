import { Component } from '@angular/core';
import {ConnectionService} from "../connection.service";

@Component({
  selector: 'app-viewer',
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.scss']
})
export class ViewerComponent {

  constructor(public service: ConnectionService) {
  }

}
