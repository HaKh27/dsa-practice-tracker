export const fakeProblems=[
    {id:1, name:"Two Sum", topic:"Hash Map", difficulty:"Easy", last_reviewed:"10-10-2026"},
    {id:2, name:"Rotting Oranges", topic:"Graph", difficulty:"Hard", last_reviewed:"10-11-2026"},
    {id:3, name:"Dijkstras", topic:"Graph", difficulty:"Medium", last_reviewed:"10-10-2026"},
    {id:4, name:"Quicksort", topic:"Sorting", difficulty:"Easy", last_reviewed:"10-10-2026"},
]   



function ProblemList({problems}){
    
    return(
        <ul>
            {problems.map((p)=><li key={p.id}>{p.name}--{p.topic}--{p.difficulty}--{p.last_reviewed}</li>)}
        </ul>
    )
}
export default ProblemList; 