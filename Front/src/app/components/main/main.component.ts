import {Component, OnInit} from '@angular/core';
import {ProviderService} from '../../services/provider.service';
import {ImageListComponent} from '../image-list/image-list.component';
import {CategoryListComponent} from '../category-list/category-list.component';
import {IFolder} from '../../models/models';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  private isLogged = false;
  categoryId: number;
  categoryChosen: boolean = false;
  folderChosen: boolean = false;

  get current_category(): string{
    return CategoryListComponent.current_category;
  }
  get current_folder(): IFolder{
    return CategoryListComponent.current_folder;
  }
  get username(): string{
    return localStorage.getItem('username');
  }

  constructor(private provider: ProviderService) {
  }

  isLoggedChange(event) {
    this.isLogged = event;
    this.categoryChosen = false;
    this.folderChosen = false;
  }

  ngOnInit() {
    if (localStorage.getItem('token')) {
      this.isLogged = true;
      // this.change.emit(this.isLogged);
    }
  }

  categoryChange(event) {
    if(event[0] == false){
      ImageListComponent.images = [];
      ImageListComponent.current_image = 0;
    }
    this.categoryId = event[1];
    this.categoryChosen = event[0];
  }

  folderChange(event) {
    this.folderChosen = event;
  }

  logout() {
    this.provider.logout().then(res => {
    });
    this.isLogged = false;
    localStorage.clear();
  }
}
