import {EventEmitter, Injectable} from '@angular/core';
import {IAuthResponse, ICategory, IImage, IPolygon, IPolygons, IFile, ILabel, IFolder} from '../models/models';
import {HttpClient} from '@angular/common/http';
import {MainService} from './main.service';

@Injectable({
  providedIn: 'root'
})
export class ProviderService extends MainService {

  public sendMessage = new EventEmitter<number>();
  // host = 'http://89.250.84.91:8000/';
  host = 'http://localhost:8000/';

  constructor(http: HttpClient) {
    super(http);
  }

  auth(username: string, password: string): Promise<IAuthResponse> {
    return this.post(this.host + 'main/login/', {
      username: username,
      password: password
    });
  }

  register(username: string, email: string, password: string): Promise<IAuthResponse> {
    return this.post(this.host + 'main/register/', {
      username: username,
      email: email,
      password: password
    });
  }

  logout(): Promise<any> {
    return this.post(this.host + 'main/logout/', {});
  }

  getImagePolygons(imageId): Promise<any[]> {
    return this.get(this.host + 'main/image/' + imageId + '/polygons/', {});
  }

  postPolygon(polygon: IPolygon): Promise<IPolygon> {
    let data = [];
    for (let point of polygon.points) {
      data.push([point.offsetX, point.offsetY]);
    }
    return this.post(this.host + 'main/polygon/', {
      points: JSON.stringify(data),
      label: polygon.label.id,
      attributes: polygon.attributes,
      image: polygon.image
    });
  }

  deletePolygon(id: number): Promise<any> {
    return this.delete(this.host + `main/polygon/${id}/`, {});
  }

  getImages(id: number): Promise<IImage[]> {
    return this.get(this.host + `main/images/${id}/`, {});
  }

  getCategories(id: number): Promise<ICategory[]> {
    return this.get(this.host + `main/folders/${id}/`, {});
  }

  getFolders(): Promise<IFolder[]> {
    return this.get(this.host + `main/folders/`, {});
  }

  getComment(id: number): Promise<any[]> {
    return this.get(this.host + `main/image/${id}/comments/`, {});
  }

  postComment(comment: string, imageId: number): Promise<any> {
    return this.post(this.host + 'main/comment/', {
      text: comment,
      image: imageId
    });
  }

  putComment(comment: string, id: number) {
    return this.put(this.host + `main/comment/${id}/`, {
      text: comment
    });
  }

  deleteComment(id: number) {
    return this.delete(this.host + `main/comment/${id}/`, {});
  }

  getLabels(): Promise<ILabel[]> {
    return this.get(this.host + `main/labels/`, {});
  }

  postLabel(labelName): Promise<ILabel> {
    return this.post(this.host + 'main/labels/', {
      name: labelName
    });
  }

  getAnalytics(id: number): Promise<any[]> {
    return this.get(this.host + `main/image/${id}/analytics/`, {});
  }

  genReport(id: number): Promise<IFile> {
    return this.get(this.host + `main/analytics/${id}/`, {});
  }
}
