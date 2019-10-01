import { BrowserModule } from '@angular/platform-browser';
import {ClassProvider, NgModule} from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LabelingComponent } from './components/labeling/labeling.component';
import { AuthFormComponent } from './components/auth-form/auth-form.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {ProviderService} from "./services/provider.service";
import {AuthInterceptor} from "./AuthInterceptor";
import { MainComponent } from './components/main/main.component';
import { PolygonListComponent } from './components/polygon-list/polygon-list.component';
import { ImageListComponent } from './components/image-list/image-list.component';
import { CategoryListComponent } from './components/category-list/category-list.component';
import { CommentComponent } from './components/comment/comment.component';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { ModuleComponent } from './module/module.component';

@NgModule({
  declarations: [
    AppComponent,
    LabelingComponent,
    AuthFormComponent,
    MainComponent,
    PolygonListComponent,
    ImageListComponent,
    CategoryListComponent,
    CommentComponent,
    AnalyticsComponent,
    ModuleComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [
    ProviderService,
    <ClassProvider> {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }],
  bootstrap: [AppComponent]
})
export class AppModule { }
