export interface IAuthResponse {
  token: string;
  username: string;
  super: boolean;
}

export class IPolygons {
  polygons: IPolygon[] = [];
}

export class IPolygon {
  id: number = -1;
  points: any[] = [];
  label: ILabel;
  name: string = '';
  attributes: string = '';
  image: number = -1;
}

export interface IImage {
  id: number;
  name: string;
  file: string;
  extra: boolean;
}

export interface IFile {
  url: string;
}

export interface ILabel {
  id: number;
  name: string;
}

export interface ICategory {
  id: number;
  name: string;
  description: string;
}

export interface IFolder {
  id: number;
  name: string;
  description: string;
}
