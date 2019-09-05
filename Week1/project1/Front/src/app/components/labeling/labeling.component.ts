import {Component, OnInit, Input} from '@angular/core';
import {ProviderService} from '../../services/provider.service';
import {IPolygons, IPolygon, ILabel} from '../../models/models';
import {ImageListComponent} from '../image-list/image-list.component';

@Component({
  selector: 'app-labeling',
  templateUrl: './labeling.component.html',
  styleUrls: ['./labeling.component.css']
})
export class LabelingComponent implements OnInit {

  @Input() categoryId: number;

  drawing = true;
  finishing = false;
  labels: ILabel[] = [];
  points = [];
  newPoints = [];
  lastPoint;
  polygons = [];
  newPolygons: IPolygons = new IPolygons();
  polygonName = '';
  polygonLabel: number;
  polygonAttributes = '';
  stats = [];

  canvas: any;
  ctx: any;
  zoomCounter = 0;
  originWidth = 550;
  originHeight = 500;
  contrastValue = 0;
  bodyWidth = 0;
  bodyHeight = 0;

  // imageDimension = { x: 0, y: 0 };
  imageCanvas: any;
  imagectx: any;
  firstLoad = true;
  imageSource = ''; // assets/img/test.JPG
  image = new Image();
  imageId: number;
  imageName = '';
  transformIndex = 1;

  constructor(private provider: ProviderService) {
  }

  ngOnInit() {
    this.bodyHeight = document.body.clientHeight;
    this.bodyWidth = document.body.clientWidth;
    if (this.bodyWidth > 1700) {
      this.originWidth = 800;
    } else {
      this.originWidth = 550;
    }
  }

  getPolygons() {
    this.provider.getImagePolygons(this.imageId).then(res => {
      if (res.length == 0) {
        ImageListComponent.images[ImageListComponent.current_image].extra = false;
      }
      for (const polygon of res) {
        const data = JSON.parse(polygon.points);
        const points = [];
        for (const dot of data) {
          points.push({offsetX: dot[0], offsetY: dot[1]});
        }
        const newPolygon = new IPolygon();
        newPolygon.id = polygon.id;
        newPolygon.label = polygon.label;
        newPolygon.name = polygon.name;
        newPolygon.attributes = polygon.attributes;
        newPolygon.image = polygon.image;
        newPolygon.points = points;
        this.newPolygons.polygons.push(newPolygon);

        const pointsVis = JSON.parse(JSON.stringify(points));
        for (const point of pointsVis) {
          point.offsetX *= this.transformIndex;
          point.offsetY *= this.transformIndex;
        }
        this.polygons.push(pointsVis);
      }
      this.fillPolygon('rgba(255, 0, 0, 0.5)');
    });

    // this.provider.getAnalytics(this.imageId).then(res => {
    //   this.stats = res;
    // });
  }

  initImage() {
    this.image.src = this.imageSource;
    this.image.crossOrigin = 'anonymous';
  }

  initCanvas() {
    this.canvas = document.getElementById('canvasMain');
    this.canvas.width = this.originWidth;
    this.canvas.height = this.originHeight;
    this.ctx = this.canvas.getContext('2d');
    this.imageCanvas = document.getElementById('canvasImage');
    this.imageCanvas.width = this.originWidth;
    this.imageCanvas.height = this.originHeight;

    this.imageDraw();
    // this.firstLoad = false;
  }

  imageDraw() {
    if (!this.firstLoad) {
      this.imagectx.clearRect(1, 1, this.imageCanvas.width, this.imageCanvas.height);
    }
    const self = this;
    self.imagectx = this.imageCanvas.getContext('2d');

    this.image.onload = function() {
      if (self.firstLoad) {
        self.transformIndex = self.originWidth / self.image.width;
        self.originHeight = self.image.height * self.transformIndex;
        self.canvas.width = self.originWidth;
        self.canvas.height = self.originHeight;
        self.imageCanvas.width = self.originWidth;
        self.imageCanvas.height = self.originHeight;

        const canvas = document.getElementById('canvas-block');
        canvas.setAttribute(
          'style', 'width: ' + (self.originWidth + 20) + 'px; height: ' + (self.originHeight + 20) + 'px;');

        self.getPolygons();
      }
      self.firstLoad = false;
      // self.drawImage(self.image);
      self.applyContrast();
      self.fillPolygon('rgba(255, 0, 0, 0.5)');
    };
  }

  drawImage(image) {
    this.imagectx.drawImage(image, 0, 0, image.width, image.height, 0, 0, this.imageCanvas.width, this.imageCanvas.height);
  }

  zoomIn() {
    if (!this.finishing) {
      this.zoomCounter += 1;
      this.zoom();
    }
  }

  zoomOut() {
    if (this.zoomCounter > -5 && !this.finishing) {
      this.zoomCounter -= 1;
      this.zoom();
    }

  }

  resetZoom() {
    this.zoomCounter = 0;
    this.zoom();
  }

  zoom() {
    this.canvas.height = this.originHeight * (1 + this.zoomCounter * 0.1);
    this.canvas.width = this.originWidth * (1 + this.zoomCounter * 0.1);
    this.imageCanvas.height = this.originHeight * (1 + this.zoomCounter * 0.1);
    this.imageCanvas.width = this.originWidth * (1 + this.zoomCounter * 0.1);

    this.initImage();
    this.imageDraw();
    this.zoomPolygon();
    if (this.drawing) {
      this.zoomPath();
    }
    this.fillPolygon('rgba(255, 0, 0, 0.5)');

    // if (this.finishing) {
    //   this.showInfoDiv();
    // }
  }

  drawPolygon() {
    this.drawing = true;
  }

  fillPolygon(color) {
    this.ctx.clearRect(1, 1, this.canvas.width, this.canvas.height);
    this.ctx.fillStyle = color;
    this.ctx.beginPath();
    this.polygons.forEach((points) => {
      points.forEach((point, index) => {
        // tslint:disable-next-line:triple-equals
        if (index == 0) {
          this.ctx.moveTo(point.offsetX, point.offsetY);
        } else {
          this.ctx.lineTo(points[index].offsetX, points[index].offsetY);
        }
      });

    });
    this.ctx.closePath();
    this.ctx.fill();
    if (this.drawing) {
      this.drawPath();
    }
  }

  refillPolygon(i, color1, color2) {
    this.ctx.clearRect(1, 1, this.canvas.width, this.canvas.height);
    this.ctx.fillStyle = color1;
    this.ctx.beginPath();
    this.polygons.forEach((points, polIndex) => {
      if (polIndex != i) {
        points.forEach((point, index) => {
          if (index == 0) {
            this.ctx.moveTo(point.offsetX, point.offsetY);
          } else {
            this.ctx.lineTo(points[index].offsetX, points[index].offsetY);
          }
        });
      }
    });
    this.ctx.closePath();
    this.ctx.fill();

    this.ctx.fillStyle = color2;
    this.ctx.beginPath();
    this.polygons[i].forEach((point, index) => {
      if (index == 0) {
        this.ctx.moveTo(point.offsetX, point.offsetY);
      } else {
        this.ctx.lineTo(this.polygons[i][index].offsetX, this.polygons[i][index].offsetY);
      }
    });
    this.ctx.closePath();
    this.ctx.fill();
    if (this.drawing) {
      this.drawPath();
    }
  }

  drawPath() {
    this.points.forEach((point, index) => {
      if (index == 0) {
        this.drawPoint(point, 'green');
      } else {
        this.drawPoint(point, 'red');
        this.drawLine(point, 'red', index);
      }
    });
  }

  zoomPolygon() {
    this.polygons.forEach((points, i) => {
      points.forEach((point, j) => {
        point.offsetX = this.newPolygons.polygons[i].points[j].offsetX * (1 + this.zoomCounter * 0.1) * this.transformIndex;
        point.offsetY = this.newPolygons.polygons[i].points[j].offsetY * (1 + this.zoomCounter * 0.1) * this.transformIndex;
      });
    });
  }

  zoomPath() {
    this.points.forEach((point, index) => {
      point.offsetX = this.newPoints[index].offsetX * (1 + this.zoomCounter * 0.1) * this.transformIndex;
      point.offsetY = this.newPoints[index].offsetY * (1 + this.zoomCounter * 0.1) * this.transformIndex;
    });
  }

  drawPoint(coords, color) {
    this.ctx.beginPath();
    this.ctx.arc(coords.offsetX, coords.offsetY, 3, 0, 2 * Math.PI);
    this.ctx.fillStyle = color;
    this.ctx.fill();
    this.ctx.lineWidth = 1;
    this.ctx.strokeStyle = 'black';
    this.ctx.stroke();
  }

  drawLine(coords, color, pointIndex) {
    const prevPoint = {offsetX: this.points[pointIndex - 1].offsetX, offsetY: this.points[pointIndex - 1].offsetY};
    this.ctx.beginPath();
    this.ctx.moveTo(prevPoint.offsetX, prevPoint.offsetY);
    this.ctx.lineTo(coords.offsetX, coords.offsetY);
    this.ctx.lineWidth = 2;
    this.ctx.strokeStyle = color;
    this.ctx.stroke();
  }

  canvasClick(e) {

    if (!this.drawing) {
      return;
    }
    const coords = {offsetX: e.offsetX, offsetY: e.offsetY};
    const newCoords = {offsetX: e.offsetX, offsetY: e.offsetY};
    newCoords.offsetX = Math.round(coords.offsetX / (1 + this.zoomCounter * 0.1) / this.transformIndex);
    newCoords.offsetY = Math.round(coords.offsetY / (1 + this.zoomCounter * 0.1) / this.transformIndex);
    if (this.points.length == 0) {
      this.drawPoint(coords, 'green');
      this.points.push(coords);
      this.newPoints.push(newCoords);
    } else if (this.points.length < 3) {
      if (!((coords.offsetX >= this.points[0].offsetX - 5 && coords.offsetX <= this.points[0].offsetX + 5) && (coords.offsetY >= this.points[0].offsetY - 5 && coords.offsetY <= this.points[0].offsetY + 5))) {
        this.drawPoint(coords, 'red');
        this.drawLine(coords, 'red', this.points.length);
        this.points.push(coords);
        this.newPoints.push(newCoords);
      }
    } else {
      this.drawPoint(coords, 'red');
      this.drawLine(coords, 'red', this.points.length);

      const firstPoint = {offsetX: this.newPoints[0].offsetX, offsetY: this.newPoints[0].offsetY};
      firstPoint.offsetX *= (1 + this.zoomCounter * 0.1) * this.transformIndex;
      firstPoint.offsetY *= (1 + this.zoomCounter * 0.1) * this.transformIndex;
      if ((coords.offsetX >= firstPoint.offsetX - 5 && coords.offsetX <= firstPoint.offsetX + 5) && (coords.offsetY >= firstPoint.offsetY - 5 && coords.offsetY <= firstPoint.offsetY + 5)) {
        this.drawing = false;
        this.finishing = true;
        this.polygons.push(this.points);
        this.fillPolygon('rgba(255, 0, 0, 0.5)');
        this.showInfoDiv(e);
        this.lastPoint = coords;
        return;
      }
      this.points.push(coords);
      this.newPoints.push(newCoords);
    }
  }

  undoPolygon() {
    if (!this.finishing) {
      this.ctx.clearRect(1, 1, this.canvas.width, this.canvas.height);
      this.points.pop();
      this.newPoints.pop();
      this.fillPolygon('rgba(255, 0, 0, 0.5)');
    } else {
      this.undoInfoDiv();
    }
  }

  deletePolygon(index) {
    this.polygons.splice(index, 1);
    const polygon = this.newPolygons.polygons.splice(index, 1)[0];
    this.provider.deletePolygon(polygon.id).then(res => {
      if (this.newPolygons.polygons.length <= 0) {
        ImageListComponent.images[ImageListComponent.current_image].extra = false;
      }
    });
    this.drawPolygon();
  }

  showInfoDiv(event) {
    const infoDiv = document.getElementById('infoDiv');
    infoDiv.setAttribute(
      'style', 'position: absolute; visibility: visible; top: ' + (event.y + 5) + 'px; left:' + (event.x - 23) + 'px;');
  }

  hideInfoDiv() {
    const attributesText = document.getElementById('attributesText') as HTMLInputElement;
    const objectText = document.getElementById('objectText') as HTMLInputElement;
    objectText.value = '';
    attributesText.value = '';
    const infoDiv = document.getElementById('infoDiv');
    infoDiv.style.visibility = 'hidden';
    this.finishing = false;
  }

  undoInfoDiv() {
    this.hideInfoDiv();
    this.points.push(this.lastPoint);
    this.polygons.pop();
    this.undoPolygon();
    this.drawing = true;
  }

  deleteInfoDiv() {
    this.hideInfoDiv();
    this.points = [];
    this.newPoints = [];
    this.polygons.pop();
    this.fillPolygon('rgba(255, 0, 0, 0.5)');
    this.drawing = true;
  }

  doneInfoDiv() {
    if (this.polygonName == '') {
      document.getElementById('objectText').style.border = '2px solid red';
      return;
    }

    const labels = this.normalizeArray(this.labels, 'name');
    if (!(this.polygonName in labels)) {
      this.provider.postLabel(this.polygonName).then(res => {
        this.labels.push(res);
        labels[this.polygonName] = res;
        this.postPolygon(labels);
      });
    } else {
      this.postPolygon(labels);
    }
  }

  postPolygon(labels) {
    document.getElementById('objectText').style.border = '1px solid rgba(0,0,0,0.3)';
    const polygon = new IPolygon();
    const points = JSON.parse(JSON.stringify(this.points));
    for (const point of points) {
      point.offsetX = Math.round(point.offsetX / (1 + this.zoomCounter * 0.1) / this.transformIndex);
      point.offsetY = Math.round(point.offsetY / (1 + this.zoomCounter * 0.1) / this.transformIndex);
    }
    polygon.points = points;
    polygon.label = labels[this.polygonName];
    polygon.name = this.polygonName;
    polygon.attributes = this.polygonAttributes;
    polygon.image = this.imageId;
    console.log(polygon);
    this.provider.postPolygon(polygon).then(res => {
      polygon.id = res.id;
      this.newPolygons.polygons.push(polygon);
      ImageListComponent.images[ImageListComponent.current_image].extra = true;
    });

    this.hideInfoDiv();
    this.points = [];
    this.newPoints = [];
    this.polygonName = '';
    this.polygonAttributes = '';
    this.drawing = true;
  }

  normalizeArray<T>(array: Array<T>, indexKey: keyof T) {
    const normalizedObject: any = {};
    for (let i = 0; i < array.length; i++) {
      const key = array[i][indexKey];
      normalizedObject[key] = array[i];
    }
    return normalizedObject as { [key: string]: T };
  }

  mContrast() {
    this.contrastValue -= 5;
    this.applyContrast();
  }

  pContrast() {
    this.contrastValue += 5;
    this.applyContrast();
  }

  resetContrast() {
    this.contrastValue = 0;
    this.applyContrast();
  }


  truncateColor(value) {
    if (value < 0) {
      value = 0;
    } else if (value > 255) {
      value = 255;
    }
    return value;
  }

  applyContrast() {
    this.drawImage(this.image);
    const imageData = this.imagectx.getImageData(0, 0, this.imageCanvas.width, this.imageCanvas.height);
    const factor = (259.0 * (this.contrastValue + 255.0)) / (255.0 * (259.0 - this.contrastValue));

    for (let i = 0; i < imageData.data.length; i += 4) {
      imageData.data[i] = this.truncateColor(factor * (imageData.data[i] - 128.0) + 128.0);
      imageData.data[i + 1] = this.truncateColor(factor * (imageData.data[i + 1] - 128.0) + 128.0);
      imageData.data[i + 2] = this.truncateColor(factor * (imageData.data[i + 2] - 128.0) + 128.0);
    }
    this.imagectx.putImageData(imageData, 0, 0);
  }

  changeImage(image) {
    this.imageId = image.id;
    this.imageName = image.name;
    this.imageSource = image.file;
    this.polygons = [];
    this.newPolygons = new IPolygons();
    this.points = [];
    this.newPoints = [];
    this.firstLoad = true;
    this.zoomCounter = 0;
    this.contrastValue = 0;

    this.provider.getLabels().then(res => {
      this.labels = res;
    });

    this.initImage();
    this.initCanvas();
    // this.getPolygons();
    this.resetZoom();
  }

}
