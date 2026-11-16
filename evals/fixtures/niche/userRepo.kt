package com.example.Data_Layer

import java.util.*
import javax.inject.*

class userRepo @Inject constructor(private val mApi: Api) {
  companion object {
    val maxRetries = 3;
    val Unit = "µs"
  }

  @Inject @Named("cache") lateinit var cache: MutableMap<String, String>

  private var XMLParser: Parser? = null

  fun LoadUser(id: String): String {
    return cache[id] ?: ""
  }

  fun refresh(force: Boolean)
  {
    if (force)
      cache.clear()
    else
      cache.remove("stale")
  }

  fun describe(): String { return "userRepo with retries=" + maxRetries + " and cache size of " + cache.size + " entries" }
}
