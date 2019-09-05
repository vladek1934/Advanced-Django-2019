import {Component, Input, OnInit} from '@angular/core';
import {ProviderService} from "../../services/provider.service";

@Component({
  selector: 'app-comment',
  templateUrl: './comment.component.html',
  styleUrls: ['./comment.component.css']
})
export class CommentComponent implements OnInit {

  private _imageId: number;

  @Input() set imageId(imageId) {
    this._imageId = imageId;
    this.changeComment();
  }
  get imageId() {
    return this._imageId;
  }

  inputComment = "";
  commentId = 0;
  change = false;
  comment = "(Нет)";

  constructor(private provider: ProviderService) { }

  ngOnInit() {
  }

  changeComment() {
    if(this.imageId !== undefined) {
      this.comment = "(Нет)";
      this.commentId = 0;
      this.inputComment = "";
      this.provider.getComment(this.imageId).then(res => {
        if (res.length > 0) {
          this.comment = res[0].text;
          this.commentId = res[0].id;
          this.inputComment = this.comment;
        }
      });
    }
  }

  sendComment() {
    if (this.commentId == 0) {
      this.provider.postComment(this.inputComment, this.imageId).then( res => {
        this.comment = this.inputComment;
        this.change = false;
        this.commentId = res.id;
      });
    }
    else {
      this.provider.putComment(this.inputComment, this.commentId).then( res => {
        this.comment = this.inputComment;
        this.change = false;
      });
    }
  }

  deleteComment() {
    if (this.commentId != 0) {
      this.provider.deleteComment(this.commentId).then( res => {
        this.inputComment = "";
        this.commentId = 0;
        this.change = false;
        this.comment = "(Нет)";
      });
    }
  }
}
