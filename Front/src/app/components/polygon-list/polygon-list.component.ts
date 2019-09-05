import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';

@Component({
  selector: 'app-polygon-list',
  templateUrl: './polygon-list.component.html',
  styleUrls: ['./polygon-list.component.css']
})
export class PolygonListComponent implements OnInit {

  @Input() polygons = [];
  @Output() highlight: EventEmitter<number> = new EventEmitter<number>();
  @Output() deHighlight: EventEmitter<any> = new EventEmitter<any>();
  @Output() delete: EventEmitter<number> = new EventEmitter<number>();

  highlighter(index) {
    this.highlight.emit(index);
  }
  deHighlighter() {
    this.deHighlight.emit();
  }
  deleter(index) {
    this.delete.emit(index);
    this.deHighlighter();
  }

  constructor() { }

  ngOnInit() {
  }

}
