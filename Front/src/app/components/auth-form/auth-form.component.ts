import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {ProviderService} from '../../services/provider.service';

@Component({
  selector: 'app-auth-form',
  templateUrl: './auth-form.component.html',
  styleUrls: ['./auth-form.component.css']
})
export class AuthFormComponent implements OnInit {

  @Output() change: EventEmitter<boolean> = new EventEmitter<boolean>();

  private isLogged = false;
  private username = '';
  private password = '';
  private error = false;

  reg = false;
  private regUsername = '';
  private regPassword1 = '';
  private regPassword2 = '';
  private regEmail = '';

  constructor(private provider: ProviderService) {
  }

  auth() {
    if (this.username !== '' && this.password !== '') {
      this.provider.auth(this.username, this.password).then(res => {
        localStorage.setItem('token', res.token);
        localStorage.setItem('username', res.username);
        localStorage.setItem('super', String(res.super));
        this.isLogged = true;
        this.error = false;
        this.change.emit(this.isLogged);
      }).catch(
        res => {
          this.error = true;
        }
      );
    }
  }

  logout() {
    this.isLogged = false;
    localStorage.clear();
    this.change.emit(this.isLogged);
    this.provider.logout().then(res => {
    });
  }

  ngOnInit() {
    if (localStorage.getItem('token')) {
      this.isLogged = true;
      // this.change.emit(this.isLogged);
    }
  }

  keyDownFunction(event) {
    if(event.keyCode == 13) {
      if (this.reg)
        this.register();
      else if (!this.reg)
        this.auth();
    }
  }

  setActive(newAct, oldAct) {
    let div1 = document.getElementById(newAct);
    let div2 = document.getElementById(oldAct);

    div1.classList.replace('inactive', 'active');
    div2.classList.replace('active', 'inactive');

    if (newAct == 'reg') {
      this.reg = true;
    }
    else if (newAct == 'auth') {
      this.reg = false;
    }
  }

  register() {
    let errMes = '';
    let errDiv = document.getElementById('error');

    if (this.regUsername === '' || this.regEmail === '' || this.regPassword1 === '' || this.regPassword2 === '') {
      errMes = "Заполните все поля и повторите попытку";
    } else {
      if (!this.regEmail.includes('@')) {
        errMes = "Некорректный E-mail"
      }
      if (this.regPassword1.length < 8) {
        errMes = "Пароль должен состоять хотя бы из 8 символов"
      }
      if (this.regPassword1 !== this.regPassword2) {
        errMes = "Пароли не совпадают"
      }
    }

    if (errMes !== ''){
      errDiv.innerHTML = errMes;
    }
    else {
      this.provider.register(this.regUsername, this.regEmail, this.regPassword1).then(res => {
        this.username = this.regUsername;
        this.password = this.regPassword1;
        this.auth();
        // this.setActive('auth', 'reg');
      }).catch(res => {
        errMes="Регистрация не удалась. Проверьте данные или повторите попытку позже";
        errDiv.innerHTML = errMes;
      })
    }
  }
}
