import {Injectable} from "@angular/core";
import {Router} from "@angular/router";
import {WebSocketSubject} from "rxjs/internal-compatibility";
import {webSocket} from "rxjs/webSocket";

@Injectable()
export class ConnectionService {

  private socket: WebSocketSubject<any>;
  private image: string;

  constructor(private router: Router) {
  }

  public connectAndSend(host: string, port: string, source: File, pattern: File): void {
    this.socket = webSocket({url: `ws://${host}:${port}/`, deserializer: e => e.data});
    const sub = this.socket.asObservable().subscribe(
      data => this.dataReceived(data),
      err => console.log(err),
      () => {
        console.log('complete');
        sub.unsubscribe();
      }
    );
    this.sendFile(pattern);
    this.sendFile(source);
  }

  private dataReceived(result): void {
    this.image = result;
    this.router.navigate(['view']);
  }

  public getImage(): string {
    return this.image;
  }

  private sendFile(file: File): void {
    const reader: FileReader = new FileReader();
    reader.onload = () => {
      this.socket.next(<string>reader.result);
    };
    reader.readAsDataURL(file);
  }

}
