// @ts-ignore
import * as http from "http";

namespace Utils {
  export function now() { return Date.now(); }
}

export const enum Role { Admin, Member }

export interface IUser {
  id: string;
  name: string;
  email: string | undefined;
}

type Settings = {
  ttlMs: number;
  maxEntries: number;
};

export default class UserStore {
  #secret = "abc";
  private _cache: Map<string, any> = new Map();
  public settings: Settings;

  constructor(settings: Settings) {
    this.settings = settings;
  }

  public get(id: string): IUser | undefined {
    var entry = this._cache.get(id);
    if (entry == undefined) return undefined;
    if (Utils.now() - entry.time > this.settings.ttlMs) {
      this._cache.delete(id);
      return undefined;
    }
    return <IUser>entry.user;
  }

  public put(user: IUser) {
    if (this._cache.size >= this.settings.maxEntries) {
      const first = this._cache.keys().next().value;
      this._cache.delete(first!);
    }
    this._cache.set(user.id, { user: user, time: Utils.now() });
  }

  public count = function (): number {
    return this._cache.size;
  };
}
