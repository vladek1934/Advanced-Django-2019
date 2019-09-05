import {Component, EventEmitter, HostListener, Input, OnInit, Output} from '@angular/core';
import {ProviderService} from '../../services/provider.service';
import {IImage} from '../../models/models';

@Component({
  selector: 'app-image-list',
  templateUrl: './image-list.component.html',
  styleUrls: ['./image-list.component.css']
})
export class ImageListComponent implements OnInit {
  get images(): IImage[] {
    return ImageListComponent.images;
  }

  get current_image(): number {
    return ImageListComponent.current_image;
  }

  constructor(private provider: ProviderService) {
  }

  static images: IImage[] = [];

  static current_image = 0;

  @Input() extra = false;
  @Input() categoryId: number;
  @Output() source: EventEmitter<IImage> = new EventEmitter<IImage>();
  images_empty = true;

  ngOnInit() {
    this.provider.getImages(this.categoryId).then(res => {
      this.images_empty = false;
      ImageListComponent.images = res;
      if (res.length > 0) {
        this.source.emit(res[0]);
      }
    });
  }


  changeImage(index) {
    this.source.emit(ImageListComponent.images[index]);
    ImageListComponent.current_image = index;
  }

  // @HostListener('document:keydown', ['$event'])
  // keyDownFunction(event: KeyboardEvent) {
  //   switch (event.key) {
  //     case 'ArrowDown':
  //       if (ImageListComponent.current_image < this.images.length - 1) {
  //         this.changeImage(ImageListComponent.current_image + 1);
  //       }
  //       break;
  //     case 'ArrowUp':
  //       if (ImageListComponent.current_image > 0) {
  //         this.changeImage(ImageListComponent.current_image - 1);
  //       }
  //       break;
  //   }
  // }

}
