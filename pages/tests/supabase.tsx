import { supabase } from "../../utils/supabase-client"

const SupabaseTest = ({ cantatas }) => {
    return (
        <div>
            {cantatas.map((cantata) => (
                <p key={cantata.id}>{cantata.title}</p>
            ))}
        </div>
    )
}

export const getStaticProps = async () => {
    const { data: cantatas } = await supabase.from('cantatas').select('*')

    return {
        props: {
            cantatas,
        },
    }
}

export default SupabaseTest
