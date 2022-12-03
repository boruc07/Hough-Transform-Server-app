import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ViewerComponent } from './viewer/viewer.component';
import { HomeComponent } from './home/home.component';
import {IonicModule} from '@ionic/angular';
import {ConnectionService} from "./connection.service";

@NgModule({
  declarations: [
    AppComponent,
    ViewerComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    IonicModule.forRoot()
  ],
  providers: [ConnectionService],
  bootstrap: [AppComponent]
})
export class AppModule { }
