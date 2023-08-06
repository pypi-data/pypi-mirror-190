import { URLExt } from "@jupyterlab/coreutils";

import { ServerConnection } from "@jupyterlab/services";

export function normalizeURL(endPoint = "") {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, endPoint);

  return requestUrl;
}

/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
export async function requestAPI<T>(
  endPoint = "",
  init: RequestInit = {}
): Promise<T> {
  // Make request to Jupyter API
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(
    settings.baseUrl,
    "globus-jupyterlab",
    endPoint
  );

  let response: Response;
  try {
    console.log("making request to: " + requestUrl);
    response = await ServerConnection.makeRequest(requestUrl, init, settings);
  } catch (error) {
    throw new ServerConnection.NetworkError(error);
  }

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }

  return await response.json();
}
