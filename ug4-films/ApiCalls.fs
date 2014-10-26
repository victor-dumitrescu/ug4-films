module ApiCalls

open FSharp.Data

let apiKey = "66pedstgeyz4wa2uycf5qf3f"

type Film = {id: string;
             title: string}

let makeFilm (j: JsonValue) =
    {id = j.Item("id").ToString()
          |> (fun x -> x.[1..x.Length-2]);
     title = j.Item("title").ToString()
             |> (fun x -> x.[1..x.Length-2])
    }


let getFilmRecord (json: JsonValue) = 
    let output = 
        match json with
        | JsonValue.Record [|total; movies; _; _ |]
            -> match movies with
               | (_, JsonValue.Array [| movie |])
                   -> movie 
                      |> makeFilm
                      |> Some
               | _ -> None
        | _ -> None

    output.Value


let getFilmByTitle title = 

    System.Threading.Thread.Sleep(100)
    Http.RequestString
        ("http://api.rottentomatoes.com/api/public/v1.0/movies.json", 
            httpMethod = "GET",
            query = [ "q", title;
                      "page_limit", "1";
                      "page", "1";
                      "apikey", apiKey] )
        |> JsonValue.Parse
        |> getFilmRecord


let getSimilarFilms id =
   
    System.Threading.Thread.Sleep(100)
    let url =  sprintf "http://api.rottentomatoes.com/api/public/v1.0/movies/%s/similar.json" id
    let json = Http.RequestString
                (url,
                 httpMethod = "GET",
                 query = [ "limit", "5";
                           "apikey", apiKey])
                |> JsonValue.Parse
    
    match json with
    | JsonValue.Record [| movies; _; _|]
        -> match movies with
            | (_, JsonValue.Array a) -> a |> Array.map makeFilm 
                                          |> Some
            | _ -> None
    | _ -> None
