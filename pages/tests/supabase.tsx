import { supabase } from "../../utils/supabase-client"
import {InferGetStaticPropsType} from "next";

const SupabaseTest = ({ cantatas }: InferGetStaticPropsType<typeof getStaticProps>) => {
    return (
        <div>
            {cantatas?.map((cantata) => (
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
