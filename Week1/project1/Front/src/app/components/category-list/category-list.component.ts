import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ProviderService} from '../../services/provider.service';
import {ICategory, IFile, IFolder} from '../../models/models';
import {ImageListComponent} from '../image-list/image-list.component';
import {DomSanitizer, SafeResourceUrl} from '@angular/platform-browser';
import {element} from 'protractor';
import {AuthFormComponent} from '../auth-form/auth-form.component';

@Component({
  selector: 'app-category-list',
  templateUrl: './category-list.component.html',
  styleUrls: ['./category-list.component.css']
})
export class CategoryListComponent implements OnInit {

  @Output() categoryChange: EventEmitter<any> = new EventEmitter<any>();
  @Output() folderChange: EventEmitter<any> = new EventEmitter<any>();
  @Input() categoryChosen: boolean = false;
  @Input() folderChosen: boolean = false;
  categories: ICategory[] = [];
  folders: IFolder[] = [];
  categories_empty = true;
  folders_empty = true;
  report: IFile;
  Url: SafeResourceUrl = '';
  reported = false;
  static current_category = '';
  static current_folder: IFolder;

  get super(): boolean {
    return JSON.parse(localStorage.getItem('super'));
  };

  get current_folder(): IFolder {
    return CategoryListComponent.current_folder;
  };

  constructor(private provider: ProviderService, private sanitizer: DomSanitizer) {
  }

  ngOnInit() {
    if (this.folderChosen == false) {
      this.provider.getFolders().then(res => {
        this.folders = res;
        this.folders_empty = false;
      });
    } else {
      this.provider.getFolders().then(res => {
        this.folders = res;
        this.folders_empty = false;
      });
      this.provider.getCategories(CategoryListComponent.current_folder.id).then(res => {
        this.categories = res;
        this.categories_empty = false;
      });
    }
  }

  chooseCategory(index) {
    this.categoryChosen = true;
    this.categoryChange.emit([true, this.categories[index].id]);
    CategoryListComponent.current_category = this.categories[index].name;
    ImageListComponent.images = [];
    ImageListComponent.current_image = 0;
  }

  chooseFolder(index) {
    this.folderChosen = true;
    this.folderChange.emit(true);
    CategoryListComponent.current_folder = this.folders[index];
    this.provider.getCategories(CategoryListComponent.current_folder.id).then(res => {
      this.categories = res;
      this.categories_empty = false;
    });
  }

  getReport(index) {
    this.provider.genReport(this.categories[index].id).then(
      res => {
        this.report = res;
        this.report.url = this.provider.host + this.report.url;
        this.Url = this.transform(this.report.url);
        this.reported = true;
      }
    );
  }

  transform(url) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }


  changeCategory() {
    if (this.categoryChosen === true) {
      this.categoryChosen = false;
      this.categoryChange.emit([false, 1]);
    } else {
      this.categoryChosen = false;
      this.categoryChange.emit([false, 1]);
      this.folderChosen = false;
      CategoryListComponent.current_folder = this.folders[0];
    }
  }
}
